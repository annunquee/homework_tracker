from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from .serializers import TeacherRegistrationSerializer, ChildCreationSerializer
from .models import Child
from .forms import TeacherRegistrationForm
from django.contrib import messages

User = get_user_model()

# Utility function to check user roles
def is_teacher(user):
    return user.is_authenticated and user.role == "teacher"

def is_child(user):
    return user.is_authenticated and user.role == "child"

def is_parent(user):
    return user.is_authenticated and user.role == "parent"

def home_page(request):
     return render(request, 'home.html')


########## TEACHER REGISTER - Only teachers can register online ###########
def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your teacher account has been created. You can now log in.')
            return redirect('login')  # Make sure this matches your login URL name
    else:
        form = TeacherRegistrationForm()  # ← This was missing in your GET case!

    return render(request, 'registration/register_teacher.html', {'form': form})

# User Login View
@csrf_exempt  # Disable CSRF for API endpoints if you haven't set it up properly
@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])  # Allow anyone to access login
def user_login_view(request):
    """
    Log in a user (teacher, parent, or child) with username and password.
    Returns their role on success.
    """
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

    elif request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Redirect based on user role
            if is_teacher(user):
                return redirect('teacher_dashboard')
            elif is_parent(user):
                return redirect('parent_dashboard')
            elif is_child(user):
                return redirect('child_dashboard')

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Dashboard Views (Protected by Role)
@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    return render(request, "homework/teacher_dashboard.html")

@login_required
@user_passes_test(is_child)
def child_dashboard(request):
    return render(request, "child_dashboard.html")

@login_required
@user_passes_test(is_parent)
def parent_dashboard(request):
    return render(request, "parent_dashboard.html")

# Create Child View
@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_child_view(request):
    """
    Creates a child user and links them to a teacher and parent.
    """
    data = request.data
    child_username = data.get("child_username")
    child_password = data.get("child_password")
    selected_parent_id = data.get("selected_parent")
    new_parent_username = data.get("new_parent_username")
    new_parent_password = data.get("new_parent_password")

    # Validate child fields
    if not child_username or not child_password:
        return Response({"error": "Child username and password are required."},
                        status=status.HTTP_400_BAD_REQUEST)

    parent_user = get_parent_user(selected_parent_id, new_parent_username, new_parent_password)

    if not parent_user:
        return Response({"error": "Parent not found or invalid data."}, status=status.HTTP_400_BAD_REQUEST)

    # Ensure the child username doesn't exist
    if User.objects.filter(username=child_username).exists():
        return Response({"error": "Child username is already in use."},
                        status=status.HTTP_400_BAD_REQUEST)

    child_user = User.objects.create(username=child_username, role='child', password=child_password)

    # Link child with parent and teacher
    Child.objects.create(child_user=child_user, teacher_id=6, parent=parent_user)

    return Response({"message": "Child user created successfully."}, status=status.HTTP_201_CREATED)

# Helper function to get or create a parent
def get_parent_user(selected_parent_id, new_parent_username, new_parent_password):
    if selected_parent_id:
        try:
            return User.objects.get(id=selected_parent_id, role='parent')
        except User.DoesNotExist:
            return None  # Parent not found
    elif new_parent_username and new_parent_password:
        if User.objects.filter(username=new_parent_username).exists():
            return None  # Username already taken
        return User.objects.create(username=new_parent_username, role='parent', password=new_parent_password)
    return None

# Fetch Existing Parents
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def existing_parents_view(request):
    """
    Fetch a list of existing parents.
    """
    parents = User.objects.filter(role='parent')
    parent_data = [{"id": parent.id, "username": parent.username} for parent in parents]
    return Response(parent_data, status=status.HTTP_200_OK)

######### REGISTER TEACHER ############
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def teacher_register_view(request):
    """
    Register a teacher and automatically log them in.
    """
    serializer = TeacherRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()  # Save the teacher user (role='teacher')

        # Authenticate the new teacher and log them in
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"message": "Teacher registered and logged in."}, status=status.HTTP_201_CREATED)
        return Response({"error": "Authentication failed after registration."}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
