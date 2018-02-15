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
        test_model = list(models.Application.objects.filter(date_updated__lte=ninety_days_ago))
        for model in test_model:
            print(str(datetime.now()) + 'Deleting application: ' + str(model.pk))
            model.delete()

