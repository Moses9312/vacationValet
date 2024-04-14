# Generated by Django 5.0.3 on 2024-04-13 12:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("employee", "0002_alter_employee_departament"),
    ]

    operations = [
        migrations.AlterField(
            model_name="department",
            name="supervisor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]