import django_filters
from django import forms

from employee.models import Employee, Department, HolidayRequest


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


class HolidayFilter(django_filters.FilterSet):
    cnp = django_filters.CharFilter(field_name='employee__cnp', lookup_expr='icontains', label='CNP',
                                    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNP'}))
    employee = django_filters.CharFilter(method='filter_employee', lookup_expr='icontains', label='Employee',
                                         widget=forms.TextInput(
                                             attrs={'class': 'form-control', 'placeholder': 'First/Last Name'}))
    start_date = django_filters.DateFilter(lookup_expr='icontains', label='Start Date',
                                           widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
                                           )
    end_date = django_filters.DateFilter(lookup_expr='icontains', label='End Date',
                                         widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    type = django_filters.ChoiceFilter(label='Holiday Type', choices=HolidayRequest.TYPE_CHOICES,
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    approval_status = django_filters.ChoiceFilter(label='Approval Status', choices=HolidayRequest.APPROVAL_CHOICES,
                                                  widget=forms.Select(attrs={'class': 'form-control'}))

    def filter_employee(self, queryset, value):
        return queryset.filter(employee__first_name__icontains=value) | queryset.filter(
            employee__last_name__icontains=value)

    class Meta:
        model = HolidayRequest
        fields = ['cnp', 'employee', 'start_date', 'end_date', 'type', 'approval_status']
