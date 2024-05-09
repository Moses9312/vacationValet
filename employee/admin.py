from django.contrib import admin
from django.contrib.auth.models import Permission

from employee.models import *

admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(HolidayRequest)
admin.site.register(TimeRecord)
admin.site.register(Permission)
