from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# Automatic deletion frequency in minutes
AUTOMATIC_DELETION_FREQUENCY = 2

# Expiry threshold for applications in days
EXPIRY_THRESHOLD = 0.04

# The interval after which an email detailing next steps is sent
NEXT_STEPS_EMAIL_DELAY_IN_DAYS = 0.0001

DEV_APPS = [
    'debug_toolbar',
]

MIDDLEWARE_DEV = [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

MIDDLEWARE = MIDDLEWARE + MIDDLEWARE_DEV
INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + DEV_APPS + PROJECT_APPS

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fwzyivx(xxab@bz6g6!v&&qv69mcv^za-vrh@nj5k!61((2aof'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB', 'postgres'),
        'USER': os.environ.get('POSTGRES_USER', 'ofsted'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'OfstedB3ta'),
        'HOST': os.environ.get('POSTGRES_HOST', '130.130.52.132'),
        'PORT': os.environ.get('POSTGRES_PORT', '5462')
    }
}

MIGRATION_MODULES = {
    'application': 'application.tests.test_migrations',
}