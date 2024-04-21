import calendar
import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView

from employee.filters import EmployeeFilter
from employee.forms import EmployeeForm, EmployeeUpdateForm
from employee.models import Employee, TimeRecord


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
    employees = Employee.objects.filter(is_superuser=False)

    # Obtinem zilele din luna curenta
    today = datetime.date.today()
    month = today.month
    year = today.year
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
    for employee in employees:
        row = []
        for day in days:
            existing_record: TimeRecord = TimeRecord.objects.filter(employee=employee, date__year=year,
                                                                    date__month=month, date__day=day).first()
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

    return render(request, 'record_time/record_time.html',
                  {'employees': employees, 'year': year, 'month': month, 'days': days, 'values': values,
                   'weekend_days': weekend_days})
