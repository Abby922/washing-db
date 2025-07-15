from django.db import models
from django.conf import settings

class Appointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    machine = models.ForeignKey('MachineStatus', on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.user.username} - {self.date} {self.start_time}-{self.end_time} @ {self.machine.name}"


from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    student_id = models.CharField(max_length=20, unique=True)
    student_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    line_id = models.CharField(max_length=50, blank=True, null=True) 

    REQUIRED_FIELDS = ['student_id', 'student_name', 'email']

    def __str__(self):
        return self.username
    
class MachineStatus(models.Model):
    name = models.CharField(max_length=10,unique=True)
    status = models.CharField(max_length=20)
    time_remaining = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name