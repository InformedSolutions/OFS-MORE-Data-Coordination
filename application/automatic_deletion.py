from application import models
from data_coordinator import settings
from datetime import datetime, timedelta

from django_cron import CronJobBase, Schedule


class automatic_deletion(CronJobBase):

    RUN_EVERY_MINS = settings.AUTOMATIC_DELETION_FREQUENCY

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'application.automatic_deletion'

    def do(self):
        ninety_days_ago = datetime.now() - timedelta(days=90)
        expired_submissions = list(models.Application.objects.exclude(application_status='COMPLETE').filter(date_updated__lte=ninety_days_ago))

        for submission in expired_submissions:
            print(str(datetime.now()) + ' - Deleting application: ' + str(submission.pk))
            submission.delete()


