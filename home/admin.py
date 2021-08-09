from django.contrib import admin
from .models import checkpost, vehicle_info, defaulter, closed_cases, staff
admin.site.register(checkpost)
admin.site.register(vehicle_info)
admin.site.register(defaulter)
admin.site.register(closed_cases)
admin.site.register(staff)
# Register your models here.
