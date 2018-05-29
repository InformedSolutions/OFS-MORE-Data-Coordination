import logging

from application import models
from application import notify
from data_coordinator import settings
from datetime import datetime, timedelta

from django_cron import CronJobBase, Schedule


class delayed_email(CronJobBase):

    RUN_EVERY_MINS = settings.AUTOMATIC_DELETION_FREQUENCY

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'application.delayed_email'

    email = str(email)

    # HEALTH
    template_id = '2cd5f1c5-4900-4922-a627-a0d1f674136b'
    # DBS as well
    template_id = 'c7500574-df3c-4df1-b7f7-8755f6b61c7f'

    personalisation = {'first_name': first_name, 'ref': ref}
    send_email(email, personalisation, template_id)
    
    def do(self):
        log = logging.getLogger('django.server')
        log.info('Checking for expired applications')
        ten_days_ago = datetime.now() - timedelta(days=10)
        delayed_email = list(models.Application.objects.exclude(application_status='COMPLETE').filter(date_updated__lte=ten_days_ago))

        for submission in delayed_email:
            print(str(datetime.now()) + ' - Sending Delayed Email: ' + str(submission.pk))
            log.info(str(datetime.now()) + ' - Sending Delayed Email: ' + str(submission.pk))
            submission.delete()


