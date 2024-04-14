import django_filters
from django import forms

from employee.models import Employee, Department


class EmployeeFilter(django_filters.FilterSet):
    cnp = django_filters.CharFilter(lookup_expr='icontains', label='CNP',
                                    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNP'}))
    first_name = django_filters.CharFilter(lookup_expr='icontains', label='First Name',
                                           widget=forms.TextInput(
                                               attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = django_filters.CharFilter(lookup_expr='icontains', label='First Name',
                                          widget=forms.TextInput(
                                              attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    username = django_filters.CharFilter(lookup_expr='icontains', label='Username', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    gender = django_filters.ChoiceFilter(label='Gender', choices=Employee.GENDER_OPTIONS,
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    email = django_filters.CharFilter(lookup_expr='icontains', label='Email',
                                      widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    departament = django_filters.ChoiceFilter(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=[(dep.id, dep.name) for dep in Department.objects.all()])


class Meta:
    model = Employee
    fields = ['cnp', 'first_name', 'last_name', 'username', 'gender', 'email', 'departament']
