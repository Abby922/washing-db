print("🟢 執行中：run_scheduler.py")

from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from booking.utils.reminders import check_upcoming_appointments, check_machines_and_notify
import logging

logging.getLogger('django.db.backends').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

def run_reminders():
    check_upcoming_appointments()
    check_machines_and_notify()

class Command(BaseCommand):
    help = '啟動 Scheduler 進行提醒'

    def handle(self, *args, **kwargs):
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            "booking.management.commands.run_scheduler:run_reminders",
            trigger="interval",
            minutes=1,
            id="remind_appointments",
            replace_existing=True,
        )

        register_events(scheduler)
        scheduler.start()
        logger.info("🔁 Scheduler started")

        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            scheduler.shutdown()