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
    GENDER_OPTIONS = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    cnp = models.IntegerField(blank=False, null=True, unique=True)
    gender = models.CharField(max_length=6, choices=GENDER_OPTIONS, null=True)
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
        return f'{self.first_name} {self.last_name}'  # Implicit mostenite din clasa AbstractUser


class HolidayRequest(models.Model):
    TYPE_CHOICES = (
        ('co', 'CO'),
        ('cev', 'CEV')
    )
    APPROVAL_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    approved = models.BooleanField(default=False)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    attachment = models.FileField(upload_to='static/holiday_request/')
    reason = models.TextField(null=True, blank=True)
    approval_status = models.CharField(max_length=50, choices=APPROVAL_CHOICES, default='pending')


class TimeRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    duration = models.DurationField(default=datetime.timedelta(hours=8))

    def __str__(self):
        return f'{self.employee} {self.date} {self.duration}'
