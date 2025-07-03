from booking.models import Appointment, CustomUser, MachineStatus
from booking.utils.line_notify import send_line_message
from datetime import datetime, timedelta

def check_upcoming_appointments():
    now = datetime.now()
    target = now + timedelta(minutes=10)
    appointments = Appointment.objects.filter(
        date=target.date(),
        start_time__hour=target.hour,
        start_time__minute=target.minute
    )

    for app in appointments:
        try:
            user = CustomUser.objects.get(student_id=app.student_id)
            if user.line_id:
                msg = f"⏰ 預約提醒：你預約的洗衣時間（{app.start_time.strftime('%H:%M')}）快到了，請準時使用洗衣機 {app.machine}！"
                send_line_message(user.line_id, msg)
        except Exception:
            continue

def check_machines_and_notify():
    running_machines = MachineStatus.objects.filter(status='運轉中')
    for machine in running_machines:
        if machine.time_remaining in ['5分鐘', '00:05', '5 min']:
            today = datetime.today().date()
            appointments = Appointment.objects.filter(
                date=today,
                machine=machine.name
            ).order_by('-start_time')

            if appointments.exists():
                app = appointments.first()
                try:
                    user = CustomUser.objects.get(student_id=app.student_id)
                    if user.line_id:
                        msg = f"🧺 洗衣快好了！洗衣機 {machine.name} 只剩 5 分鐘，請準備來拿衣服 👕"
                        send_line_message(user.line_id, msg)
                except:
                    continue