from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

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

