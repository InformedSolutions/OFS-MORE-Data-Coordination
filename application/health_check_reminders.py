import logging

from .notify import send_email
from datetime import datetime
from .business_logic import generate_list_of_adults_not_completed_health_check
from . import utils

from django.conf import settings
from django_cron import CronJobBase, Schedule
from .services.db_gateways import HMGatewayActions, IdentityGatewayActions


log = logging.getLogger(__name__)


class HealthCheckReminderEmail(CronJobBase):

    schedule = Schedule(run_every_mins=settings.HEALTH_CHECK_REMINDER_FREQ_MINS)
    code = 'application.health_check_reminders'

    def do(self):
        """
        Function for sending a reminder email detailing next steps to an applicant
        """
        with utils.CronErrorContext():
            send_second_reminder = generate_list_of_adults_not_completed_health_check(settings.SECOND_HEALTH_CHECK_REMINDER_THRESHOLD)
            send_third_reminder = generate_list_of_adults_not_completed_health_check(settings.THIRD_HEALTH_CHECK_REMINDER_THRESHOLD)
	    log.info('sending ' + str(len(send_second_reminder)) + ' second reminders')
	    log.info('sending ' + str(len(send_third_reminder)) + ' third reminders')

            # send second reminder email
            for adult in send_second_reminder:
                with utils.CronErrorContext():
                    adult_id = adult['adult_id']
                    token_id = adult['token_id']
                    log.info('Adult ID: ' + str(adult_id))

                    dpa_auth_response = HMGatewayActions().read('dpa-auth', params={'token_id': token_id})
                    if dpa_auth_response.status_code == 200:
                        record = dpa_auth_response.record
                        applicant_name = record['first_name'] + " " + record['last_name']
                    else:
                        applicant_name = ''

                    adult_name = adult['first_name']

                    log.info(str(datetime.now()) + ' - Sending second health check reminder: ' + str(adult_id))
                    template_id = 'a9cf45d9-ab54-4c49-afa1-59b7cebb334f'
                    email = adult['email']
                    log.info(email)
                    base_url = settings.HM_EMAIL_VALIDATION_URL
                    token = adult['token']
                    link = base_url + "/" + token
                    log.info(base_url)
                    personalisation = {"firstName": adult_name,
                                       "ApplicantName": applicant_name,
                                       "link": link

                                       }

                    r = send_email(email, personalisation, template_id, service_name="New adults in the home")
                    log.info(r)
                    if r.status_code not in (200, 201):
                            raise ConnectionError(r.status_code)
                    adult['second_health_check_reminder_sent'] = True
                    HMGatewayActions().put('adult', params=adult)
                    log.info("Sending second health check reminder email")

            # send third reminder email
            for adult in send_third_reminder:
                with utils.CronErrorContext():
                    adult_id = adult['adult_id']
                    token_id = adult['token_id']
                    log.info('Adult ID: ' + str(adult_id))

                    dpa_auth_response = HMGatewayActions().read('dpa-auth', params={'token_id': token_id})
                    if dpa_auth_response.status_code == 200:
                        record = dpa_auth_response.record
                        applicant_name = record['first_name'] + " " + record['last_name']
                        applicant_first_name = record['first_name']
                    else:
                        applicant_name = ''
                        applicant_first_name = ''

                    adult_name = adult['first_name']
                    adult_full_name = adult['first_name'] + " " + adult['last_name']

                    log.info(str(datetime.now()) + ' - Sending second health check reminder: ' + str(adult_id))
                    adult_template_id = 'a9cf45d9-ab54-4c49-afa1-59b7cebb334f'
                    adult_email = adult['email']
                    log.info(email)
                    base_url = settings.HM_EMAIL_VALIDATION_URL
                    token = adult['token']
                    link = base_url + "/" + token
                    log.info(base_url)
                    adult_email_personalisation = {"firstName": adult_name,
                                       "ApplicantName": applicant_name,
                                       "link": link

                                       }

                    r = send_email(adult_email, adult_email_personalisation, adult_template_id, service_name="New adults in the home")
                    log.info("Sending third health check reminder email to adult")
                    log.info(r)
                    if r.status_code not in (200, 201):
                        raise ConnectionError(r.status_code)
                    cm_email_personalisation = { 'ApplicantFirstName': applicant_first_name,
                                                 'NewAdultFullName': adult_full_name}

                    cm_template_id = "3e12c3ce-4c5f-4271-bd91-6fa4f1e91e13"
                    cm_email = IdentityGatewayActions().read('user_details', params={'application_id': token_id}).record['email']
                    r = send_email(cm_email, cm_email_personalisation, cm_template_id, service_name="New adults in the home")
                    log.info(r)
                    if r.status_code not in (200, 201):
                        raise ConnectionError(r.status_code)
                    adult['third_health_check_reminder_sent'] = True
                    HMGatewayActions().put('adult', params=adult)
                    log.info("Sending third health check reminder email to childminder")


