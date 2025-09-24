from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django.utils import timezone
from datetime import timedelta
from .models import Appointment, CustomUser
from .utils.line_notify import send_line_message

def notify_upcoming_appointments():
    now = timezone.now()
    upcoming_time = now + timedelta(minutes=10)
    print(f"🔔 Scheduler check at {now.strftime('%H:%M:%S')}")

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
                print(f"🔔 Sending reminder to {user.student_name} for {appointment.start_time}")
        except CustomUser.DoesNotExist:
            continue

# 在啟動階段設定 scheduler
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
scheduler.add_job(
    notify_upcoming_appointments,
    trigger=IntervalTrigger(minutes=1),
    id="notify_upcoming_appointments",
    replace_existing=True,
)