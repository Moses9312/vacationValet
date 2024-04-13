import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100)
    supervisor = models.ForeignKey('Employee', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Employee(AbstractUser):
    gender_options = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    # departament_options = (
    #     ('frontend', 'Frontend'),
    #     ('backend', 'Backend'),
    #     ('cc', 'Call Center'),
    #     ('devops', 'DevOps'),
    #     ('engineering', 'Software Engineering')
    # )

    # first_name = models.CharField(max_length=40)
    # last_name = models.CharField(max_length=40)
    cnp = models.IntegerField(blank=False, null=True, unique=True)
    # email = models.EmailField(max_length=60, unique=True)
    # active = models.BooleanField(default=True)
    gender = models.CharField(max_length=6, choices=gender_options, null=True)
    birth_date = models.DateField(null=True, blank=False)
    departament = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True, blank=True)
    notice_date = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    is_supervisor = models.BooleanField(default=False)
    days_off = models.IntegerField(default=21, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class HolidayRequest(models.Model):
    TYPE_CHOICES = (
        ('co', 'CO'),
        ('cev', 'CEV')
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    approved = models.BooleanField(default=False)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    attachment = models.FileField(upload_to='static/holiday_request/')
    reason = models.TextField(null=True, blank=True)


class TimeRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    duration = models.DurationField(default=datetime.timedelta(hours=8))
