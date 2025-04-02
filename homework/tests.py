from django.test import TestCase
from users.models import User  # Ensure correct import
from homework.forms import CustomUserCreationForm  # Import from homework
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFormsTests(TestCase):
    def setUp(self):
        # Set up a user for the tests
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_custom_user_creation_form_valid_data(self):
        form_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())  # Ensure form validation passes
