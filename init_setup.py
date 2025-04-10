import os
import django
from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homework_tracker.settings')
django.setup()

# STEP 1: Migrate users app first (important for custom user model)
execute_from_command_line(["manage.py", "migrate", "users", "--noinput"])

# STEP 2: Migrate the rest
execute_from_command_line(["manage.py", "migrate", "--noinput"])
print("✅ Migrations applied successfully.")

# STEP 3: Create superuser
User = get_user_model()
if not User.objects.filter(username=os.getenv("DJANGO_SUPERUSER_USERNAME")).exists():
    User.objects.create_superuser(
        username=os.getenv("DJANGO_SUPERUSER_USERNAME"),
        email=os.getenv("DJANGO_SUPERUSER_EMAIL"),
        password=os.getenv("DJANGO_SUPERUSER_PASSWORD"),
    )
    print("✅ Superuser created successfully.")
else:
    print("⚠️ Superuser already exists. Skipping creation.")
