from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, View, UpdateView, DetailView

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

        '''
        Verificarea si generarea automata a unei adrese de e-mail in DB dupa combinatia "nume.prenume"
        '''

        # Se verifica daca angajatul are 2 sau mai multe prenume
        first_name_parts = instance.first_name.split()
        if len(first_name_parts) > 1:
            first_name = first_name_parts[0].lower()
        else:
            first_name = instance.first_name.lower()

        # Generarea adresei de email dupa combinatia "prenume.nume@gmail.com"
        email = f"{first_name}.{instance.last_name.lower()}@gmail.com"

        # Se verifica daca e-mail mai exista in baza de date,
        # daca mai exista atunci ii va genera e-mail "prenume1.nume" s.a.m.d.
        existing_emails = Employee.objects.filter(email=email)
        if existing_emails.exists():
            index = 1
            while True:
                new_email = f"{first_name}{index}.{instance.last_name.lower()}@gmail.com"
                if not Employee.objects.filter(email=new_email).exists():
                    email = new_email
                    break
                index += 1

        instance.email = email
        instance.save()
        return super().form_valid(form)


class EmployeeListView(ListView):
    template_name = 'employee/list_of_employees.html'
    model = Employee
    context_object_name = 'all_employees'

    def get_queryset(self):
        return Employee.objects.filter(active=True)


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
