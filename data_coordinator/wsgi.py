"""
WSGI config for data_coordinator project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import logging

log = logging.getLogger(__name__)
log.info('Data Coordinator Started')
log.info("(NB: If you're looking to run the cron tasks, you should run `cronbash.sh` or add it to the crontab)")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_coordinator.settings")
application = get_wsgi_application()
