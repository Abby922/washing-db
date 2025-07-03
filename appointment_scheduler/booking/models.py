from django.db import models

class Appointment(models.Model):
    student_id = models.CharField(max_length=20)  # 或者使用 IntegerField() 如果 ID 是整数
    name = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateField()
    machine = models.CharField(max_length=100)  # 為 machine 欄位指定正確的類型
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"Student ID: {self.student_id} - {self.name} - {self.date} {self.start_time} to {self.end_time} - Machine: {self.machine}"


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