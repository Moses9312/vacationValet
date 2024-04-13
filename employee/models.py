from django.db import models


class Employee(models.Model):
    gender_options = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    departament_options = (
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('cc', 'Call Center'),
        ('devops', 'DevOps'),
        ('engineering', 'Software Engineering')
    )

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    cnp = models.IntegerField(blank=False, null=False, unique=True)
    email = models.EmailField(max_length=60, unique=True)
    active = models.BooleanField(default=True)
    gender = models.CharField(max_length=6, choices=gender_options)
    departament = models.CharField(max_length=11, choices=departament_options)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    notice_date = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    is_supervisor = models.BooleanField(default=False)
    days_off = models.IntegerField(default=21, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
