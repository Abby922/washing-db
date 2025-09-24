from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-0=f!wsb^0kr(j^2bz8_-=g#^j)w0s&1=56s$s(865r^1i(1i=f"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS=['localhost', '127.0.0.1','django-backend-ezvd.onrender.com']

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    'django.contrib.staticfiles',
    "booking",
    'django.contrib.sites',
    'django_apscheduler',
]

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = "appointment_scheduler.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'django.template.context_processors.request',  # 确保添加这一行
                'booking.context_processors.add_dynamic_version'
            ],
        },
    },
]

WSGI_APPLICATION = "appointment_scheduler.wsgi.application"


import dj_database_url
import os

DATABASES = {}
DATABASE_URL = os.getenv("EXTERNAL_DB_URL") or os.getenv("INTERNAL_DB_URL")
if DATABASE_URL:
    DATABASES["default"] = dj_database_url.parse(DATABASE_URL, conn_max_age=600)
else:
    raise Exception("No DATABASE_URL found in environment.")


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]



LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'booking.CustomUser'
LOGIN_REDIRECT_URL = '/booking/'
LOGOUT_REDIRECT_URL = '/login/'

SITE_ID = 1

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a" 

SCHEDULER_CONFIG = {
    'apscheduler.jobstores.default': {
        'type': 'django_apscheduler.jobstores:DjangoJobStore',
    },
    'apscheduler.executors.default': {
        'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        'max_workers': '20'
    },
    'apscheduler.executors.processpool': {
        'class': 'apscheduler.executors.pool:ProcessPoolExecutor',
        'max_workers': '5'
    },
    'apscheduler.job_defaults.coalesce': 'false',
    'apscheduler.job_defaults.max_instances': '1',
    'apscheduler.timezone': 'UTC',
}

import os
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',  # 🔄 改成 INFO，這樣 DEBUG 就不會印出來
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',  # ✅ 保留在檔案裡的完整 debug 訊息
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django_debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',    # 🔕 關掉 SQL 的 DEBUG 訊息，只印出錯誤
            'propagate': False,
        },
        'apscheduler': {
            'handlers': ['console', 'file'],
            'level': 'INFO',       # 🔄 改成 INFO 只看必要的工作記錄
            'propagate': False,
        },
    },
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR/"booking"/"static",
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

import os
import dj_database_url

USE_INTERNAL_DB = os.getenv("USE_INTERNAL_DB", "True").lower() == "true"

DATABASE_URL = os.getenv("INTERNAL_DB_URL") if USE_INTERNAL_DB else os.getenv("EXTERNAL_DB_URL")

