# Generated by Django 5.0.3 on 2024-04-27 08:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("employee", "0005_remove_holidayrequest_approved"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="employee",
            name="is_supervisor",
        ),
    ]
