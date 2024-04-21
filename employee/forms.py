from datetime import date, timedelta

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import TextInput, NumberInput, EmailInput, Select, DateInput, Textarea, PasswordInput, FileInput
from django.views.generic import DeleteView

from employee.models import Employee, TimeRecord, HolidayRequest
import calendar


class EmployeeForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'cnp', 'gender', 'birth_date', 'username', 'password1', 'password2',
                  'email',
                  'departament', 'start_date', 'end_date', 'address']
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'Enter employee first name', 'class': 'form-control'}),
            'last_name': TextInput(attrs={'placeholder': 'Enter employee last name', 'class': 'form-control'}),
            'cnp': NumberInput(
                attrs={'placeholder': 'Enter employee last 6 numbers of ID number', 'class': 'form-control'}),
            'gender': Select(attrs={'class': 'form-control'}),
            'birth_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'username': TextInput(attrs={'placeholder': 'Enter employee username', 'class': 'form-control'}),
            # 'password': PasswordInput(attrs={'placeholder': 'Enter employee password', 'class': 'form-control'}),
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

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs = {'class': 'form-control', 'placeholder': 'Password'}
        self.fields['password2'].widget.attrs = {'class': 'form-control', 'placeholder': 'Confirm Password'}


class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'cnp', 'gender', 'birth_date', 'username', 'email',
                  'departament',
                  'start_date', 'end_date', 'notice_date', 'address', 'days_off']

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
            'notice_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': Textarea(
                attrs={'placeholder': 'State, City, Street, Floor, Apartament... ', 'class': 'form-control',
                       'rows': 3}),
            'days_off': NumberInput(attrs={'class': 'form-control'})

        }


class AuthenticationNewForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password'})


class TimeRecordForm(forms.ModelForm):
    class Meta:
        model = TimeRecord
        fields = '__all__'

        widgets = {
            'employee': Select(attrs={'class': 'form-control'}),
            'date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'duration': NumberInput(attrs={'class': 'form-control'}),
        }


class MonthSelectionForm(forms.Form):
    months = [(i, calendar.month_name[i]) for i in range(1, 13)]
    month = forms.ChoiceField(choices=months)


class HolidayRequestForm(forms.ModelForm):
    class Meta:
        model = HolidayRequest
        exclude = ['approval_status']

        widgets = {
            'employee': Select(attrs={'class': 'form-control'}),
            'start_date': DateInput(
                attrs={'class': 'form-control', 'type': 'date', 'id': 'id_start_date', 'min': str(date.today())}),
            'end_date': DateInput(
                attrs={'class': 'form-control', 'type': 'date', 'id': 'id_end_date',
                       'min': str(date.today())}),
            'type': Select(attrs={'class': 'form-control'}),
            'attachment': FileInput(attrs={'class': 'form-control'}),
            'reason': TextInput(attrs={'class': 'form-control'})
        }
