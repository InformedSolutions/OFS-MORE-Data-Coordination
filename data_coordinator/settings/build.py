from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# Automatic deletion frequency is done in minutes
AUTOMATIC_DELETION_FREQUENCY = 10

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
    'django.server': {
        'level': 'INFO',
        'class': 'logging.handlers.RotatingFileHandler',
        'maxBytes': 1 * 1024 * 1024,
        'filename': '/source/logs/output.log',
        'formatter': 'console',
        'maxBytes': 1 * 1024 * 1024,
        'backupCount': 30
    },
   },
   'loggers': {
     '': {
       'handlers': ['django.server'],
         'level': 'INFO',
           'propagate': True,
      },
    },
}