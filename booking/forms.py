from django import forms
from .models import Appointment,MachineStatus
import datetime


class AppointmentForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
    )
    choices = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple,
    )
    machine = forms.ModelChoiceField(
        queryset=MachineStatus.objects.all(),
        required=True,
        empty_label=None,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        choices = []
        start = datetime.datetime.strptime('00:00', '%H:%M')
        while start < datetime.datetime.strptime('23:59', '%H:%M'):
            end = start + datetime.timedelta(minutes=30)
            choices.append((f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')}", f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')}"))
            start = end

        self.fields['choices'].choices = choices

    def clean_choices(self):
        choices = self.cleaned_data.get('choices')
        if len(choices) > 2:
            raise forms.ValidationError('You can only select up to two time slots')
        return choices

    def clean(self):
        cleaned_data = super().clean()
        choices = cleaned_data.get('choices')

        if choices:
            existing_appointments = Appointment.objects.filter(user__student_id=self.user.student_id)
            total_appointments = len(existing_appointments) + len(choices)

            if total_appointments > 2:
                raise forms.ValidationError('You can only have up to two time slots in total.')

        return cleaned_data

    def save(self, commit=True):
        appointments = []
        machine = self.cleaned_data.get('machine')  # 获取选择的机台
        for choice in self.cleaned_data.get('choices', []):
            start_time_str, end_time_str = choice.split(' - ')
            start_time = datetime.datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.datetime.strptime(end_time_str, '%H:%M').time()

            appointment = Appointment(
                name=self.user.get_full_name() if self.user else '',
                email=self.user.email if self.user else '',
                student_id=self.user.student_id if self.user else '',
                date=self.cleaned_data['date'],
                start_time=start_time,
                end_time=end_time,
                machine=machine  # 将选择的机台存储到预约中
            )
            if commit:
                appointment.save()
            appointments.append(appointment)

        return appointments

    class Meta:
        model = Appointment
        fields = ['date', 'choices', 'machine']
        

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    student_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'student_id', 'student_name', 'email', 'password1', 'password2')
