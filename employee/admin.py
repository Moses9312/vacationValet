from django.contrib import admin

from employee.models import *

admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(HolidayRequest)
admin.site.register(TimeRecord)
