# Generated by Django 5.0.3 on 2024-04-01 20:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("employee", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="end_date",
            field=models.DateField(null=True),
        ),
    ]
