import logging
import random
import string

from application.business_logic import generate_expiring_applications_list_cm_applications, \
    generate_expiring_applications_list_nanny_applications, generate_list_of_expired_cm_applications, \
    generate_list_of_expired_nanny_applications
from application.notify import send_email
from .models import Application, UserDetails, applicant_name
from django.conf import settings
from datetime import datetime, timedelta
from application.services.db_gateways import IdentityGatewayActions

from django_cron import CronJobBase, Schedule


class automatic_deletion(CronJobBase):

    RUN_EVERY_MINS = settings.AUTOMATIC_DELETION_FREQUENCY

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'application.automatic_deletion'

    def do(self):
        log = logging.getLogger('django.server')
        log.info('Checking for expired  and expiring applications')
        send_reminder_cm = generate_expiring_applications_list_cm_applications()
        send_reminder_nanny = generate_expiring_applications_list_nanny_applications()
        expired_cm_applications = generate_list_of_expired_cm_applications()
        expired_nanny_applications = generate_list_of_expired_nanny_applications()

        for cm_application in send_reminder_cm:
            if cm_application.application_expiry_email_sent is False:
                log.info(str(datetime.now()) + ' - Sending reminder email: ' + str(cm_application.pk))
                log.info(cm_application.application_id)

                template_id = 'b52414b8-afb4-4b6b-8b10-d87efa2714f4'
                email = UserDetails.objects.get(application_id=cm_application).email
                base_url = settings.PUBLIC_APPLICATION_URL
                email.magic_link_email = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(
                    string.digits)])
                email.magic_link_email = email.magic_link_email.upper()
                log.info(email, base_url, email.magic_link_email)
                personalisation = {"link": base_url + '/validate/' + email.magic_link_email,
                                   "first_name": applicant_name}
                log.info(personalisation['link'])
                r = send_email(email, personalisation, template_id)
                cm_application.application_expiry_email_sent = True
                log.info(r)
                cm_application.save()
                email.save()

        for nanny_application in send_reminder_nanny:
            if nanny_application.application_expiry_email_sent is False:
                log.info(str(datetime.now()) + ' - Sending reminder email: ' + str(nanny_application.pk))
                log.info(nanny_application.application_id)

                template_id = '3751bbf7-fbe7-4289-a3ed-6afbd2bab8bf'
                email = IdentityGatewayActions().read('user_details', params={'application_id': nanny_application}).email
                base_url = settings.PUBLIC_APPLICATION_URL
                email.magic_link_email = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(
                    string.digits)])
                email.magic_link_email = email.magic_link_email.upper()
                log.info(email, base_url, email.magic_link_email)
                personalisation = {"link": base_url + '/validate/' + email.magic_link_email,
                                   "first_name": applicant_name}
                log.info(personalisation['link'])
                r = send_email(email, personalisation, template_id)
                nanny_application.application_expiry_email_sent = True
                log.info(r)
                nanny_application.save()
                email.save()

        for cm_application in expired_cm_applications:

            log.info(str(datetime.now()) + ' - Deleting application: ' + str(cm_application.pk))

            # Delete Application, with the deletion of associated records handled by on_delete=models.CASCADE in the
            # ForeignKey
            cm_application.delete()

        for nanny_application in expired_nanny_applications:

            log.info(str(datetime.now()) + ' - Deleting application: ' + str(nanny_application.pk))

            # Delete Application, with the deletion of associated records handled by on_delete=models.CASCADE in the
            # ForeignKey
            nanny_application.delete()
