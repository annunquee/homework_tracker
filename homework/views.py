from django.shortcuts import render


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import now
from .models import DailyHomework, HomeworkTask, ChildProgress
from .forms import DailyHomeworkForm, HomeworkTaskFormSet
 



# Helper Functions
def is_teacher(user):
    """Check if the user is a teacher"""
    return user.is_authenticated and user.role == "teacher"

def is_child(user):
    """Check if the user is a child"""
    return user.is_authenticated and user.role == "child"

def is_parent(user):
    """Check if the user is a parent"""
    return user.is_authenticated and user.role == "parent"

################################TEACHER FUNCTIONALITY #############################
# Teacher: Create Homework this stores the daily homework and tasks into the DB
#@login_required
#@user_passes_test(is_teacher)
def create_homework(request):
    if request.method == "POST":
        homework_form = DailyHomeworkForm(request.POST)
        # Use a blank instance of DailyHomework so the formset can attach
        homework_instance = DailyHomework(teacher=request.user)
        task_formset = HomeworkTaskFormSet(request.POST, instance=homework_instance)

        if homework_form.is_valid() and task_formset.is_valid():
            # Save the DailyHomework
            daily_homework = homework_form.save(commit=False)
            daily_homework.teacher = request.user
            daily_homework.save()

            # Now save the tasks, linking them to the saved daily_homework
            task_formset.instance = daily_homework
            task_formset.save()

            return redirect("teacher_dashboard")
    else:
        # GET request: Display empty forms
        homework_form = DailyHomeworkForm()
        # Provide an empty DailyHomework object so the formset knows how to link tasks
        homework_instance = DailyHomework(teacher=request.user)
        task_formset = HomeworkTaskFormSet(instance=homework_instance)

    return render(request, "homework/create_homework.html", {
        "homework_form": homework_form,
        "task_formset": task_formset,
    })

# This function forwards to the teacher dashboard i.e. the teacher homepage
#@login_required
#@user_passes_test(is_teacher)
def teacher_dashboard(request):
    # e.g., list all homework created by this teacher
    homeworks = DailyHomework.objects.filter(teacher=request.user).order_by('-date')
    return render(request, 'homework/teacher_dashboard.html', {'homeworks': homeworks})


def homework_detail(request, pk):
    homework = get_object_or_404(DailyHomework, pk=pk)
    tasks = homework.tasks.all()  # Adjust if your model relation is different
    return render(request, 'homework/homework_detail.html', {'homework': homework, 'tasks': tasks})


def home(request):
    return render(request, "home.html")  # This will look for a template named home.html


#############################CHILD FUNCTIONALITY ######################################
