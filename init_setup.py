import os
import django
from django.core.management import execute_from_command_line, call_command
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homework_tracker.settings')
django.setup()

# STEP 1 & 2: Migrate the apps
try:
    # Migrate users app first (custom user model)
    execute_from_command_line(["manage.py", "migrate", "users", "--noinput"])

    # Migrate the rest
    execute_from_command_line(["manage.py", "migrate", "--noinput"])
    print("✅ Migrations applied successfully.")

except Exception as e:
    print(f"❌ Migration failed: {e}")

# STEP 3: Create superuser
try:
    User = get_user_model()
    username = os.getenv("DJANGO_SUPERUSER_USERNAME")
    if username and not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=os.getenv("DJANGO_SUPERUSER_EMAIL"),
            password=os.getenv("DJANGO_SUPERUSER_PASSWORD"),
        )
        print("✅ Superuser created successfully.")
    else:
        print("⚠️ Superuser already exists or username env var is missing.")
except Exception as e:
    print(f"❌ Superuser creation failed: {e}")
