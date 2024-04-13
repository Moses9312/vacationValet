from django import forms
from django.forms import TextInput, NumberInput, EmailInput, Select, DateInput, Textarea
from django.views.generic import DeleteView

from employee.models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        # fields = '__all__'
        exclude = ['is_supervisor', 'days_off', 'end_date', 'notice_date', 'active', 'email']
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'Enter employee first name', 'class': 'form-control'}),
            'last_name': TextInput(attrs={'placeholder': 'Enter employee last name', 'class': 'form-control'}),
            'cnp': NumberInput(attrs={'placeholder': 'Enter employee personal ID number', 'class': 'form-control'}),
            # 'email': EmailInput(attrs={'placeholder': 'Enter employee email', 'class': 'form-control'}),
            'gender': Select(attrs={'class': 'form-control'}),
            'departament': Select(attrs={'class': 'form-control'}),
            'start_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': Textarea(
                attrs={'placeholder': 'State, City, Street, Floor, Apartament... ', 'class': 'form-control',
                       'rows': 3}),


        }

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)

        get_address = cleaned_data['address']

        if len(get_address) < 20:
            msg = 'You need to write at least 20 characters !'
            self._errors['address'] = self.error_class([msg])

        return cleaned_data


class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'Enter employee first name', 'class': 'form-control'}),
            'last_name': TextInput(attrs={'placeholder': 'Enter employee last name', 'class': 'form-control'}),
            'cnp': NumberInput(attrs={'placeholder': 'Enter employee personal ID number', 'class': 'form-control'}),
            'email': EmailInput(attrs={'placeholder': 'Enter employee email', 'class': 'form-control'}),
            'gender': Select(attrs={'class': 'form-control'}),
            'departament': Select(attrs={'class': 'form-control'}),
            'start_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notice_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': Textarea(
                attrs={'placeholder': 'State, City, Street, Floor, Apartament... ', 'class': 'form-control',
                       'rows': 3}),
            'days_off': NumberInput(attrs={'class': 'form-control'})

        }

