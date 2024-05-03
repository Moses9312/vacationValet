import calendar
import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView

from employee.filters import EmployeeFilter, HolidayFilter
from employee.forms import EmployeeForm, EmployeeUpdateForm, HolidayRequestForm
from employee.models import Employee, TimeRecord, HolidayRequest, Department


# Create your views here.

class EmployeeCreateView(LoginRequiredMixin, CreateView):
    template_name = 'employee/create_employee.html'
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        instance = form.save(commit=False)

        '''
        Verificarea si salvarea numelui si a prenumelui in DB
        '''

        # Elimina spatiile din nume si prenume
        instance.first_name = instance.first_name.strip()
        instance.last_name = instance.last_name.strip()

        # Inlocuieste '-' dintre nume si prenume cu 'space'
        instance.first_name = instance.first_name.replace('-', ' ')
        instance.last_name = instance.last_name.replace('-', ' ')

        # Numele si Prenumele se vor scrie in DB cu prima litera majuscula
        instance.first_name = instance.first_name.title()
        instance.last_name = instance.last_name.title()

        # Generarea unui CNP in functie de "Gender" (1 sau 2 sau 5 sau 6), si de data nasterii.
        gender = instance.gender
        birth_date = instance.birth_date
        if gender == 'male':
            if birth_date.year < 2000:
                cnp_start = '1'
            else:
                cnp_start = '5'
        else:
            if birth_date.year < 2000:
                cnp_start = '2'
            else:
                cnp_start = '6'
        year = str(birth_date.strftime('%y'))
        month = str(birth_date.month).zfill(2)
        day = str(birth_date.day).zfill(2)
        cnp_first_sever = cnp_start + year + month + day

        cnp_last_six = str(form.cleaned_data['cnp'])
        new_cnp = cnp_first_sever + cnp_last_six

        instance.cnp = new_cnp
        instance.save()
        return super().form_valid(form)


class EmployeeListView(LoginRequiredMixin, ListView):
    template_name = 'employee/list_of_employees.html'
    model = Employee
    context_object_name = 'all_employees'

    def get_queryset(self):
        return Employee.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        employees = Employee.objects.filter(is_superuser=False)
        myfilter = EmployeeFilter(self.request.GET, queryset=employees)
        employees = myfilter.qs
        data['all_employees'] = employees
        data['filter'] = myfilter.form

        return data


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'employee/update_employee.html'
    model = Employee
    form_class = EmployeeUpdateForm
    success_url = reverse_lazy('list-employees')


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'employee/delete_employee.html'
    model = Employee
    success_url = reverse_lazy('list-employees')


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    template_name = 'employee/details_employee.html'
    model = Employee


@login_required
def record_time_view(request):
    current_user = request.user  # Utilizatorul logat
    current_employee = Employee.objects.get(username=current_user.username)
    department = current_employee.departament

    if current_user.is_superuser:
        # Dacă utilizatorul este admin, obținem toti angajatii
        employees = Employee.objects.filter(is_superuser=False)
    else:
        # Altfel, obținem angajații din același departament cu angajatul curent
        employees = Employee.objects.filter(departament=department, is_superuser=False)

    # Obtinem zilele din luna curenta
    today = timezone.now()

    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))

    num_days = calendar.monthrange(year, month)[1]
    days = [i for i in range(1, num_days + 1)]

    # Calcul zile de weekend din luna curenta
    first_day = datetime.date(year, month, 1)
    last_day = datetime.date(year, month, num_days)
    weekend_days = [day for day in range(first_day.day, last_day.day + 1) if
                    datetime.date(year, month, day).weekday() in [5, 6]]

    if request.method == 'POST':
        for k in request.POST:
            if k.startswith('pontaj_'):
                employee_id_and_date = k[7:]
                employee_id_str, date_str = employee_id_and_date.split('_')
                hours = request.POST[k]
                time_record, created = TimeRecord.objects.get_or_create(employee_id=employee_id_str, date=date_str)
                if hours != '':
                    time_record.duration = datetime.timedelta(hours=float(hours))
                    print(employee_id_and_date)
                    print(f'logged {hours} hours')
                else:
                    time_record.duration = datetime.timedelta(hours=0)
                time_record.save()

    values = []
    enableds = []
    for employee in employees:
        row = []
        row_enabled = []
        for day in days:
            today = timezone.datetime(year, month, day).date()
            existing_holiday = HolidayRequest.objects.filter(employee=employee, approval_status='approved',
                                                             start_date__lte=today,
                                                             end_date__gte=today).first()
            existing_record: TimeRecord = TimeRecord.objects.filter(employee=employee, date__year=year,
                                                                    date__month=month, date__day=day).first()
            if day == 25:
                pass
            if month == 4:
                pass
            print(f'Holiday for {employee} on {today} {existing_holiday is not None}')
            if existing_holiday is not None:
                row_enabled.append(False)
            else:
                row_enabled.append(True)

            if existing_record is not None:
                seconds = existing_record.duration.total_seconds()
                hours = seconds / 3600
                if hours == 0:
                    row.append('')
                elif hours == int(hours):
                    row.append(int(hours))
                else:
                    row.append(hours)
            else:
                row.append('')
        values.append(row)
        enableds.append(row_enabled)

    return render(request, 'record_time/record_time.html',
                  {'employees': employees, 'year': year, 'month': month, 'days': days, 'values': values,
                   'weekend_days': weekend_days, 'years': [2024, 2025],
                   'months': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 'enableds': enableds})


class HolidayRequestCreateView(LoginRequiredMixin, CreateView):
    template_name = 'rest_holidays/add_leave_request.html'
    model = HolidayRequest
    form_class = HolidayRequestForm
    success_url = reverse_lazy('home_page')


class HolidayRequestUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'rest_holidays/approve_leave_request.html'
    model = HolidayRequest
    form_class = HolidayRequestForm
    success_url = reverse_lazy('list-requests')


class HolidayRequestListView(LoginRequiredMixin, ListView):
    template_name = 'rest_holidays/holiday_request_list.html'
    model = HolidayRequest
    context_object_name = 'holiday_requests'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return HolidayRequest.objects.all()
        else:
            departaments = Department.objects.filter(supervisor=self.request.user)
            members = Employee.objects.filter(department__in=departaments)
            requests = HolidayRequest.objects.filter(employee__in=members)
            return requests

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        requests = HolidayRequest.objects.all()
        myfilter = HolidayFilter(self.request.GET, queryset=requests)
        requests = myfilter.qs
        data['holiday_requests'] = requests
        data['filter'] = myfilter.form

        return data


def approve_requests(request):
    id = request.POST.get('id')
    approve = int(request.POST.get('approve', 0))
    holiday_request = HolidayRequest.objects.get(id=id)
    if approve == 1:
        holiday_request.approval_status = 'approved'
    else:
        holiday_request.approval_status = 'rejected'
    holiday_request.save()
    return redirect('list-requests')


# def update_days_off(request):
#     holiday_request_id = request.POST.get('id')
#     holiday_request = HolidayRequest.objects.get(id=holiday_request_id)
#
#     if holiday_request.approval_status == 'approved':
#         num_days = (holiday_request.end_date - holiday_request.start_date).days + 1
#
#         # Obține ID-ul angajatului asociat cererii de concediu
#         employee_id = holiday_request.employee_id
#
#         # Obține obiectul Employee asociat cererii de concediu
#         employee = Employee.objects.get(id=employee_id)
#
#         # Actualizează numărul de zile de concediu al angajatului
#         employee.days_off -= num_days
#         employee.save()
#
#     return redirect('list-requests')
