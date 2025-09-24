from django.apps import AppConfig
import logging
import os

class BookingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'booking'

    def ready(self):
        logging.info('Running initial tasks...')
