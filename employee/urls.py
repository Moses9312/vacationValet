from django.urls import path

from employee import views

urlpatterns = [
    path('create_employee/', views.EmployeeCreateView.as_view(), name='create-employee'),
    path('list_employees/', views.EmployeeListView.as_view(), name='list-employees'),
    path('update_employee/<int:pk>/', views.EmployeeUpdateView.as_view(), name='update-employee'),
    path('delete_employee/<int:pk>/', views.EmployeeDeleteView.as_view(), name='delete-employee'),
    path('details_employee/<int:pk>/', views.EmployeeDetailView.as_view(), name='details-employee'),
    path('record-time/', views.record_time_view, name='record-time'),
    path('add-leave-request/', views.HolidayRequestCreateView.as_view(), name='add-leave-request'),
    path('approve-leave-request/<int:pk>/', views.HolidayRequestUpdateView.as_view(), name='approve-leave-request'),
    path('list_requests/', views.HolidayRequestListView.as_view(), name='list-requests'),
    path('approve-request', views.approve_requests, name='approve-request'),
]
