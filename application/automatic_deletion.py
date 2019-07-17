import logging
import random
import string
import time

from .notify import send_email
from .models import Application, ApplicantName, UserDetails
from django.conf import settings
from datetime import datetime, timedelta

from django_cron import CronJobBase, Schedule
from . import utils

from .business_logic import generate_expiring_applications_list_cm_applications, generate_list_of_expired_cm_applications

log = logging.getLogger(__name__)


class AutomaticDeletion(CronJobBase):

    RUN_EVERY_MINS = settings.AUTOMATIC_DELETION_FREQUENCY

    schedule = Schedule(run_every_mins=1)
    code = 'application.automatic_deletion'

    def do(self):
        log.info('Checking for expired  and expiring applications')

        self._childminder_expiry_warnings()
        self._childminder_deletions()

    def _childminder_expiry_warnings(self):

        send_reminder_cm = generate_expiring_applications_list_cm_applications()

        for cm_application in send_reminder_cm:

            if cm_application.application_expiry_email_sent:
                log.debug('Already sent')
                continue

            log.info(str(datetime.now()) + ' - Sending reminder email: ' + str(cm_application.pk))
            log.info(cm_application.application_id)

            template_id = 'b52414b8-afb4-4b6b-8b10-d87efa2714f4'
            user = UserDetails.objects.get(application_id=cm_application)
            try:
                name_model = ApplicantName.objects.get(application_id=cm_application)
            except ApplicantName.DoesNotExist:
                # applicant might not have got as far as completing personal details
                name_model = None
            if name_model and name_model.first_name:
                applicant_first_name = name_model.first_name
            else:
                applicant_first_name = 'applicant'
            base_url = settings.CHILDMINDER_EMAIL_VALIDATION_URL
            user.magic_link_email = ''.join([random.choice(string.ascii_letters + string.digits)
                                             for n in range(12)])
            user.magic_link_email = user.magic_link_email.upper()
            # "expiry date" is actually creation time as epoch seconds
            user.email_expiry_date = int(time.time())
            log.info((user, base_url, user.magic_link_email))
            personalisation = {"link": base_url + '/validate/' + user.magic_link_email,
                                   "first_name": applicant_first_name}
            log.info(personalisation['link'])
            r = send_email(user.email, personalisation, template_id, service_name='Childminder')
            log.info(r)
            if r.status_code not in (200, 201):
                raise ConnectionError(r.status_code)
            cm_application.application_expiry_email_sent = True
            cm_application.save()
            user.save()

    def _childminder_deletions(self, error_context):

        expired_cm_applications = generate_list_of_expired_cm_applications()

        for cm_application in expired_cm_applications:
            log.info(str(datetime.now()) + ' - Deleting application: ' + str(cm_application.pk))

            # Delete Application, with the deletion of associated records handled by on_delete=models.CASCADE in the
            # ForeignKey
            cm_application.delete()
