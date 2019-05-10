"""
Django settings for data_coordinator project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

AUTOMATIC_DELETION_FREQ_MINS = 120

SEND_EMAIL_POLL_MINS = 1

HEALTH_CHECK_REMINDER_FREQ_MINS = 120

# Expiry threshold for applications in days
NANNY_EXPIRY_THRESHOLD = os.environ.get("NANNY_EXPIRY_THRESHOLD", 60)

# Expiry threshold for applications in days
CHILDMINDER_EXPIRY_THRESHOLD = os.environ.get("CHILDMINDER_EXPIRY_THRESHOLD", 60)

# Warning before expiry email threshold for applications
WARNING_EMAIL_THRESHOLD_DAYS = float(os.environ.get('WARNING_EMAIL_THRESHOLD', 55))

# The interval after which an email detailing next steps is sent
NEXT_STEPS_EMAIL_DELAY_IN_DAYS = float(os.environ.get('NEXT_STEPS_EMAIL_DELAY_IN_DAYS', 10))

# Base URL of notify gateway
NOTIFY_URL = os.environ.get('APP_NOTIFY_URL')

CHILDMINDER_EMAIL_VALIDATION_URL = os.environ.get('CHILDMINDER_EMAIL_VALIDATION_URL')
NANNY_EMAIL_VALIDATION_URL = os.environ.get('NANNY_EMAIL_VALIDATION_URL')

# Base URL of nanny gateway
APP_NANNY_GATEWAY_URL = os.environ.get('APP_NANNY_GATEWAY_URL')

# Base URL of identity gateway
APP_IDENTITY_URL = os.environ.get('APP_IDENTITY_URL')

HM_EMAIL_VALIDATION_URL = os.environ.get('HM_EMAIL_VALIDATION_URL')

EXECUTING_AS_TEST = os.environ.get('EXECUTING_AS_TEST')

SECOND_HEALTH_CHECK_REMINDER_THRESHOLD = 5
THIRD_HEALTH_CHECK_REMINDER_THRESHOLD = 10

# Application definition

BUILTIN_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_cron',
]

PROJECT_APPS = [
    'application.apps.ApplicationConfig',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CRON_CLASSES = [
    "application.resend_email.ResendEmail",
    "application.delayed_email.DelayedEmail",
    "application.automatic_deletion.AutomaticDeletion"
]

ROOT_URLCONF = 'data_coordinator.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'data_coordinator.wsgi.application'

# Test outputs
TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
TEST_OUTPUT_VERBOSE = True
TEST_OUTPUT_DESCRIPTIONS = True
TEST_OUTPUT_DIR = 'xmlrunner'

MIGRATION_MODULES = {'application': 'application.tests.test_migrations'}

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1 * 1024 * 1024,
            'filename': BASE_DIR + '/logs/output.log',
            'formatter': 'console',
            'backupCount': 30
        },
        'console': {
            'level': 'DEBUG',
            'formatter': 'console',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
