# Generated by Django 5.0.3 on 2024-04-21 09:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("employee", "0004_holidayrequest_approval_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="holidayrequest",
            name="approved",
        ),
    ]
