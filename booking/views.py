from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Appointment, MachineStatus
from .forms import AppointmentForm
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden

ALLOWED_IDS_FILE_PATH = r"C:\Users\abby\Desktop\洗衣機\GPT創預約系統\appointment_scheduler\booking\allowed_ids.txt"


def is_allowed_student_id(student_id):
    """检查学生 ID 是否在允许注册的列表中"""
    with open(ALLOWED_IDS_FILE_PATH, 'r') as file:
        allowed_ids = file.read().splitlines()
    return student_id in allowed_ids


@login_required(login_url='/booking/login/')
def book_appointment(request):
    # 获取当前用户的预约记录
    existing_appointments = Appointment.objects.filter(student_id=request.user.student_id)
    existing_appointmentsNum = len(existing_appointments)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, user=request.user)
        if form.is_valid():
            date = form.cleaned_data['date']
            choices = form.cleaned_data['choices']
            machine = form.cleaned_data['machine']  # 获取选中的机器
            
            # 计算总预约时间段数
            total_appointments = len(existing_appointments) + len(choices)

            if total_appointments > 2:
                # 超过两个时间段，添加错误消息并重新渲染表单
                messages.error(request, 'You can only select up to two time slots.')
                return render(request, 'booking/book_appointment.html', {
                    'form': form,
                    'existing_appointments': existing_appointments,
                    'machine_statuses': MachineStatus.objects.all()
                })

            # 循环处理每个选中的时间段
            for choice in choices:
                start_time_str, end_time_str = choice.split(' - ')
                start_time = datetime.strptime(start_time_str, '%H:%M').time()
                end_time = datetime.strptime(end_time_str, '%H:%M').time()

                # Create and save appointment using the current user
                appointment = Appointment(
                    name=request.user.student_name,  # Use user's full name
                    email=request.user.email,        # Use user's email
                    student_id=request.user.student_id,  # Use user's student_id
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                    machine=machine  # Add machine to the appointment
                )
                appointment.save()

            return redirect('success')
    else:
        form = AppointmentForm(user=request.user)

    # Pass existing appointments and machine statuses to the template
    machine_statuses = MachineStatus.objects.all()

    return render(request, 'booking/book_appointment.html', {
        'form': form,
        'existing_appointments': existing_appointments,
        'existing_appointmentsNum': existing_appointmentsNum,
        'machine_statuses': machine_statuses
    })


@login_required(login_url='/booking/login/')
def delete_appointment(request, appointment_id):
    # 获取要删除的预约对象
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if appointment.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("你沒有權限刪除這筆預約")

    if request.method == 'POST':
        appointment.delete()
        return redirect('book_appointment')  # 重定向回预约列表页面

    return render(request, 'confirm_delete.html', {'appointment': appointment})

from django.utils.dateparse import parse_date
def get_reserved_slots(request):
    # 取得日期參數
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'error': 'Date parameter is required.'}, status=400)

    # 解析日期
    date = parse_date(date_str)
    if not date:
        return JsonResponse({'error': 'Invalid date format. Expected format: YYYY-MM-DD'}, status=400)

    # 取得機器參數
    machine = request.GET.get('machine')  # 假設前端傳遞的是 machine_id
    if not machine:
        return JsonResponse({'error': 'Machine parameter is required.'}, status=400)

    try:
        # 查詢指定日期和機器下的已預定時間段
        reserved_slots = Appointment.objects.filter(date=date, machine=machine).values_list('start_time', 'end_time')

        # 格式化時間段為 "HH:MM - HH:MM"
        reserved_slots = [
            f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')}" for start, end in reserved_slots
        ]

    except Exception as e:
        return JsonResponse({'error': f'Unexpected error occurred: {str(e)}'}, status=500)

    # 回傳 JSON 格式的時間段
    return JsonResponse(reserved_slots, safe=False)

def success(request):
    return render(request, 'booking/success.html')


from django.contrib.auth import login
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        student_id = request.POST.get('student_id')
        if form.is_valid() and is_allowed_student_id(student_id):
            user = form.save(commit=False)
            user.student_name = form.cleaned_data['student_name']
            user.email = form.cleaned_data['email']
            user.save()
            login(request, user)
            return redirect('login')
        else:
            form.add_error(None, 'Invalid student ID')
    else:
        form = CustomUserCreationForm()
    return render(request, 'booking/register.html', {'form': form})

