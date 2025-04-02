from django.test import TestCase
from .models import Profile
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFormsTests(TestCase):
    def setUp(self):
        # Set up a user and profile for the tests
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user)  # Create profile if needed

    def test_custom_user_creation_form_valid_data(self):
        form_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "phone": "1234567890",
            "address": "123 Main St",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())  # Ensure form validation passes
