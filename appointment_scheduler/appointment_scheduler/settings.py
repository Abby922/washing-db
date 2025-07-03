
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-0=f!wsb^0kr(j^2bz8_-=g#^j)w0s&1=56s$s(865r^1i(1i=f"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

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

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'washing_db',
        'USER': 'postgres',
        'PASSWORD': '911222',
        'HOST': 'localhost',
        'PORT': '5432',  # PostgreSQL 的預設 port
    }
}
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/




LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django Allauth settings
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]


AUTH_USER_MODEL = 'booking.CustomUser'
LOGIN_REDIRECT_URL = '/booking/'
LOGOUT_REDIRECT_URL = '/login/'

SITE_ID = 1

# settings.py

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"  # Default

# Configure the APScheduler
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
            'level': 'DEBUG',      # ✅ 保持 DEBUG 以寫入檔案
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

import os
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

# ALLOWED_HOSTS = ['*']