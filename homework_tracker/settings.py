"""
Django settings for homework_tracker project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
import os
import dj_database_url

# Load environment variables from the .env file
load_dotenv()

# BASE_DIR definition
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY setup
SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')  # Default for local development

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Allowable hosts for production/deployment
ALLOWED_HOSTS = ['localhost', '127.0.0.1',  'homework_tracker.onrender.com']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',  # Custom user app
    'homework',  # Homework-related app
    'games',  # Games-related app
]

# Ensure ROOT_URLCONF is set correctly
ROOT_URLCONF = 'homework_tracker.urls'

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',  # Ensure this is correctly placed
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Ensure correct order
    'django.contrib.messages.middleware.MessageMiddleware',  # Ensure correct order
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Template configuration for admin
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # You can add template directories here if you want custom templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'homework_tracker.wsgi.application'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'  # URL for serving static files
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Custom static directory inside the project
]


DATABASES = {
    "default": dj_database_url.config(default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")}  # Loads connection string from DATABASE_URL

# User model configuration
AUTH_USER_MODEL = os.getenv('AUTH_USER_MODEL', 'users.User')  # Custom user model (from users app)

