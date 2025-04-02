from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Create your tests here.

class UserFormsTests(TestCase):
    def setUp(self):
        # Set up a user and profile for the tests
        self.user = User.objects.create_user(username='testuser', password='12345')
       
