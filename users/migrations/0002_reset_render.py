from django.db import migrations, connection

def drop_conflicting_tables(apps, schema_editor):
    with connection.cursor() as cursor:
        # Replace with your actual table names as needed
        tables = ["users_child", "homework_dailyhomework", "homework_homeworktask", "homework_childprogress"]
        for table in tables:
            try:
                cursor.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE;')
                print(f"Dropped table {table}")
            except Exception as e:
                print(f"Could not drop {table}: {e}")

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(drop_conflicting_tables),
    ]
