import os
import django
from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homework_tracker.settings')
django.setup()

try:
    # Migrate users app first (custom user model and Child model)
    execute_from_command_line(["manage.py", "migrate", "users", "--noinput"])

    # Migrate homework app (depends on users.Child)
    execute_from_command_line(["manage.py", "migrate", "homework", "--noinput"])

    # Migrate everything else
    execute_from_command_line(["manage.py", "migrate", "--noinput"])
    print("✅ All migrations applied.")
except Exception as e:
    print(f"❌ Migration failed: {e}")
    exit(1)

# Create superuser
try:
    User = get_user_model()
    username = os.getenv("DJANGO_SUPERUSER_USERNAME")
    if username and not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=os.getenv("DJANGO_SUPERUSER_EMAIL"),
            password=os.getenv("DJANGO_SUPERUSER_PASSWORD"),
        )
        print("✅ Superuser created.")
    else:
        print("⚠️ Superuser already exists or env var is missing.")
except Exception as e:
    print(f"❌ Superuser creation failed: {e}")
