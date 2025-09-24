from django.contrib import admin
from .models import Appointment
from .models import MachineStatus
from django_apscheduler.models import DjangoJob

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'get_user_email', 'date', 'start_time','end_time')

    def get_user_name(self, obj):
        return obj.user.username
    get_user_name.short_description = 'Name'

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'Email'


class MachineStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'time_remaining')
    search_fields = ('name', 'status')

    
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(MachineStatus, MachineStatusAdmin)