from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, View, UpdateView, DetailView

from employee.filters import EmployeeFilter
from employee.forms import EmployeeForm, EmployeeUpdateForm
from employee.models import Employee


# Create your views here.

class EmployeeCreateView(CreateView):
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


class EmployeeListView(ListView):
    template_name = 'employee/list_of_employees.html'
    model = Employee
    context_object_name = 'all_employees'

    def get_queryset(self):
        return Employee.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        employees = Employee.objects.filter(is_active=True)
        myfilter = EmployeeFilter(self.request.GET, queryset=employees)
        employees = myfilter.qs
        data['all_employees'] = employees
        data['filter'] = myfilter.form

        return data


class EmployeeUpdateView(UpdateView):
    template_name = 'employee/update_employee.html'
    model = Employee
    form_class = EmployeeUpdateForm
    success_url = reverse_lazy('list-employees')


class EmployeeDeleteView(DeleteView):
    template_name = 'employee/delete_employee.html'
    model = Employee
    success_url = reverse_lazy('list-employees')


class EmployeeDetailView(DetailView):
    template_name = 'employee/details_employee.html'
    model = Employee
