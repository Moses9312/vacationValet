import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.dispatch import receiver


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
    is_supervisor = models.BooleanField(default=False, blank=True, null=True)
    days_off = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'  # Implicit mostenite din clasa AbstractUser

    # @property - este folosit pentru a defini o metoda a unei clase ca si atribut de tip proprietate.
    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    @property
    def is_supervisor(self):
        # Verifică dacă angajatul este supraveghetor pentru vreun departament
        return Department.objects.filter(supervisor=self).exists()

    @property
    def supervisor_departments(self):
        # Returnează lista de departamente pentru care angajatul este spv
        return Department.objects.filter(supervisor=self)

    @property
    def calculate_holiday_days(self):
        if self.start_date:
            # Se calculeaza nr de luni de la angajare pana in ziua curenta.
            today = timezone.now().date()
            months_since_start = (today.year - self.start_date.year) * 12 + (today.month - self.start_date.month)

            # Se calculeaza nr de zile in functie de nr de luni
            total_holiday_days = round(months_since_start * 1.75)
            return total_holiday_days
        else:
            return 0


@receiver(pre_save, sender=Employee)
def update_employee_holiday_days(sender, instance, **kwargs):
    instance.days_off = instance.calculate_holiday_days


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
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    attachment = models.FileField(upload_to='holiday_request/', null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    approval_status = models.CharField(max_length=50, choices=APPROVAL_CHOICES, default='pending')

    def __str__(self):
        return f'{self.employee} {self.start_date} {self.end_date}'


@receiver(pre_save, sender=HolidayRequest)
def update_days_off(sender, instance, **kwargs):
    if instance.pk is None:  # Verificăm dacă este o cerere nouă de concediu
        # Calculăm numărul de zile între start_date și end_date
        num_days = (instance.end_date - instance.start_date).days + 1
        # Actualizăm numărul de zile CO ale angajatului
        instance.employee.days_off -= num_days
        instance.employee.save()


class TimeRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    duration = models.DurationField(default=datetime.timedelta(hours=8))

    def __str__(self):
        return f'{self.employee}{self.date} {self.duration}'
