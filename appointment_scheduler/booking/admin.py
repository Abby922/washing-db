from django.contrib import admin
from .models import Appointment
from .models import MachineStatus
from django_apscheduler.models import DjangoJob

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date', 'start_time','end_time')


class MachineStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'time_remaining')
    search_fields = ('name', 'status')

    
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(MachineStatus, MachineStatusAdmin)