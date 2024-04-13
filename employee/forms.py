from django import forms
from django.forms import TextInput, NumberInput, EmailInput, Select, DateInput, Textarea
from django.views.generic import DeleteView

from employee.models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'cnp', 'gender', 'birth_date', 'username', 'email', 'departament',
                  'start_date', 'end_date', 'address']
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'Enter employee first name', 'class': 'form-control'}),
            'last_name': TextInput(attrs={'placeholder': 'Enter employee last name', 'class': 'form-control'}),
            'cnp': NumberInput(
                attrs={'placeholder': 'Enter employee last 6 numbers of ID number', 'class': 'form-control'}),
            'gender': Select(attrs={'class': 'form-control'}),
            'birth_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'username': TextInput(attrs={'placeholder': 'Enter employee username', 'class': 'form-control'}),
            'email': EmailInput(attrs={'placeholder': 'Enter employee email', 'class': 'form-control'}),
            'departament': Select(attrs={'class': 'form-control'}),
            'start_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': Textarea(
                attrs={'placeholder': 'State, City, Street, Floor, Apartament... ', 'class': 'form-control',
                       'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)

        # Verificarea unicitatii a adresei de e-mail in DB

        get_email = cleaned_data['email']

        check_emails = Employee.objects.filter(email=get_email)
        if check_emails:
            msg = 'Employee with this email already exists'
            self._errors['email'] = self.error_class([msg])

        # Minim 10 caractere la adresa

        get_address = cleaned_data['address']

        if len(get_address) < 10:
            msg = 'You need to write at least 10 characters !'
            self._errors['address'] = self.error_class([msg])

        return cleaned_data


class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'cnp', 'gender', 'birth_date', 'username', 'email', 'departament',
                  'start_date', 'end_date', 'address', 'days_off']

        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'Enter employee first name', 'class': 'form-control'}),
            'last_name': TextInput(attrs={'placeholder': 'Enter employee last name', 'class': 'form-control'}),
            'cnp': NumberInput(
                attrs={'placeholder': 'Enter employee last 6 numbers of ID number', 'class': 'form-control'}),
            'gender': Select(attrs={'class': 'form-control'}),
            'birth_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'username': TextInput(attrs={'placeholder': 'Enter employee username', 'class': 'form-control'}),
            'email': EmailInput(attrs={'placeholder': 'Enter employee email', 'class': 'form-control'}),
            'departament': Select(attrs={'class': 'form-control'}),
            'start_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': Textarea(
                attrs={'placeholder': 'State, City, Street, Floor, Apartament... ', 'class': 'form-control',
                       'rows': 3}),
            'days_off': NumberInput(attrs={'class': 'form-control'})

        }
