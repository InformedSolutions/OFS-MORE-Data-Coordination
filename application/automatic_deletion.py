import logging
import random
import string
import time

from django_cron import CronJobBase, Schedule
from django.conf import settings

from application.business_logic import generate_expiring_applications_list_cm_applications, \
    generate_expiring_applications_list_nanny_applications, generate_list_of_expired_cm_applications, \
    generate_list_of_expired_nanny_applications
from application.notify import send_email
from .models import Application, UserDetails, ApplicantName
from datetime import datetime, timedelta
from application.services.db_gateways import IdentityGatewayActions, NannyGatewayActions
from . import utils


log = logging.getLogger(__name__)


class AutomaticDeletion(CronJobBase):

    RUN_EVERY_MINS = settings.AUTOMATIC_DELETION_FREQ_MINS

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'application.automatic_deletion'

    def do(self):
        with utils.CronErrorContext() as error_context:
            log.info('Checking for expired  and expiring applications')

            with error_context.sub():
                self._childminder_expiry_warnings(error_context)
            with error_context.sub():
                self._nanny_expiry_warnings(error_context)
            with error_context.sub():
                self._childminder_deletions(error_context)
            with error_context.sub():
                self._nanny_deletions(error_context)

    def _childminder_expiry_warnings(self, error_context):

        send_reminder_cm = generate_expiring_applications_list_cm_applications()

        for cm_application in send_reminder_cm:
            with error_context.sub():

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

    def _nanny_expiry_warnings(self, error_context):

        send_reminder_nanny = generate_expiring_applications_list_nanny_applications()

        for nanny_application in send_reminder_nanny:
            with error_context.sub():

                if nanny_application['application_expiry_email_sent']:
                    log.debug('Already sent')
                    continue

                log.info(str(datetime.now()) + ' - Sending reminder email: ' + nanny_application['application_id'])
                log.info(nanny_application['application_id'])

                template_id = '3751bbf7-fbe7-4289-a3ed-6afbd2bab8bf'
                response = IdentityGatewayActions().read('user',
                                                         params={'application_id': nanny_application['application_id']})
                if response.status_code != 200:
                    raise ConnectionError(response.status_code)
                user = response.record

                response = NannyGatewayActions().read('applicant-personal-details',
                                                      params={'application_id': nanny_application['application_id']})
                if response.status_code == 200:
                    personal = response.record
                elif response.status_code == 404:
                    personal = None
                else:
                    raise ConnectionError(response.status_code)

                if personal and personal['first_name']:
                    applicant_first_name = personal['first_name']
                else:
                    applicant_first_name = 'applicant'

                base_url = settings.NANNY_EMAIL_VALIDATION_URL
                user['magic_link_email'] = ''.join([random.choice(string.ascii_letters + string.digits)
                                                   for n in range(12)])
                user['magic_link_email'] = user['magic_link_email'].upper()
                # "expiry date" is actually creation time as epoch seconds
                user['email_expiry_date'] = int(time.time())
                log.info((user, base_url, user['magic_link_email']))
                personalisation = {"link": base_url + '/validate/' + user['magic_link_email'],
                                   "first_name": applicant_first_name}
                log.info(personalisation['link'])
                r = send_email(user['email'], personalisation, template_id, service_name='Nannies')
                if r.status_code not in (200, 201):
                    raise ConnectionError(r.status_code)
                log.info(r)
                nanny_application['application_expiry_email_sent'] = True
                response = NannyGatewayActions().put('application', nanny_application)
                if response.status_code != 200:
                    raise ConnectionError(response.status_code)
                response = IdentityGatewayActions().put('user', user)
                if response.status_code != 200:
                    raise ConnectionError(response.status_code)

    def _childminder_deletions(self, error_context):

        expired_cm_applications = generate_list_of_expired_cm_applications()

        for cm_application in expired_cm_applications:
            with error_context.sub():
                log.info(str(datetime.now()) + ' - Deleting application: ' + str(cm_application.pk))

                # Delete Application, with the deletion of associated records handled by on_delete=models.CASCADE in the
                # ForeignKey
                cm_application.delete()

    def _nanny_deletions(self, error_context):

        expired_nanny_applications = generate_list_of_expired_nanny_applications()

        for nanny_application in expired_nanny_applications:
            with error_context.sub():
                log.info(str(datetime.now()) + ' - Deleting application: ' + str(nanny_application['application_id']))

                # Delete Application, with the deletion of associated records handled by on_delete=models.CASCADE in the
                # ForeignKey
                response = NannyGatewayActions().delete('application',
                                                        params={'application_id': nanny_application['application_id']})
                if response.status_code not in (200, 204):
                    raise ConnectionError(response.status_code)
