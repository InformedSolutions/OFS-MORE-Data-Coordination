import logging

from .models import Application
from django.conf import settings
from datetime import datetime, timedelta

from django_cron import CronJobBase, Schedule


class automatic_deletion(CronJobBase):
    RUN_EVERY_MINS = settings.AUTOMATIC_DELETION_FREQUENCY

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'application.automatic_deletion'

    def do(self):
        log = logging.getLogger('django.server')
        log.info('Checking for expired applications')
        ninety_days_ago = datetime.now() - timedelta(days=90)
        expired_submissions = list(
            Application.objects.exclude(application_status='COMPLETE').filter(date_last_accessed__lte=ninety_days_ago))

        for submission in expired_submissions:
            print(str(datetime.now()) + ' - Deleting application: ' + str(submission.pk))
            log.info(str(datetime.now()) + ' - Deleting application: ' + str(submission.pk))
            submission.delete()
