# Generated by Django 4.2 on 2025-04-02 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('homework', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyhomework',
            name='teacher',
            field=models.ForeignKey(limit_choices_to={'role': 'teacher'}, on_delete=django.db.models.deletion.CASCADE, related_name='homework', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='childprogress',
            name='child',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.child'),
        ),
        migrations.AddField(
            model_name='childprogress',
            name='homework_task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homework.homeworktask'),
        ),
    ]
