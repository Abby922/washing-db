from datetime import datetime, timedelta
from .models import Appointment, CustomUser
from .utils.line_notify import send_line_message

def notify_upcoming_appointments():
    now = datetime.now()
    upcoming_time = now + timedelta(minutes=10)
    
    appointments = Appointment.objects.filter(
        date=now.date(),
        start_time__hour=upcoming_time.hour,
        start_time__minute=upcoming_time.minute
    )

    for appointment in appointments:
        try:
            user = CustomUser.objects.get(student_id=appointment.student_id)
            if user.line_id:
                message = f"👕 Hi {user.student_name}，你預約的洗衣時間快到了（{appointment.start_time.strftime('%H:%M')}）！"
                send_line_message(user.line_id, message)
        except CustomUser.DoesNotExist:
            continue