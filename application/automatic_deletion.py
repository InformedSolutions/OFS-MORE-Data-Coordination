from application import models
from datetime import datetime, timedelta

from django_cron import CronJobBase


class MyCronJob(CronJobBase):

    def automatic_deletion():
        ninety_days_ago = datetime.now() - timedelta(days=90)

        test_model = list(models.Application.objects.filter(date_updated__lte=ninety_days_ago))
        for model in test_model:
            print('Deleting application: ' + str(model.pk))
            model.delete()


    if __name__ == 'main':
        automatic_deletion()
