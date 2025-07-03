from django.apps import AppConfig
import logging
import os

class BookingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'booking'

    def ready(self):
        from booking.tasks import scheduler
        from booking.tasks import test_func, delete_expired_appointments  # 确保任务被导入

       
        # if os.environ.get('RUN_MAIN', None) != 'true':
            # 手动运行任务一次
        logging.info('Running initial tasks...')
        test_func()
        delete_expired_appointments()
        scheduler.start()
