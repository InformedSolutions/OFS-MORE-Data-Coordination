import logging
import random
import string

from application.business_logic import generate_expiring_applications_list_cm_applications
from application.notify import send_email
from .models import Application, UserDetails, applicant_name
from django.conf import settings
from datetime import datetime, timedelta
from application.services.db_gateways import NannyGatewayActions

from django_cron import CronJobBase, Schedule


class automatic_deletion(CronJobBase):

    RUN_EVERY_MINS = settings.AUTOMATIC_DELETION_FREQUENCY

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'application.automatic_deletion'

    def do(self):
        log = logging.getLogger('django.server')
        log.info('Checking for expired  and expiring applications')
        send_reminder = generate_expiring_applications_list_cm_applications()
        expiry_threshold = datetime.now() - timedelta(days=settings.EXPIRY_THRESHOLD)
        # Determine expired applications based on date last accessed
        expired_submissions = list(
            Application.objects.filter(application_status='DRAFTING', date_last_accessed__lte=expiry_threshold))

        for application in send_reminder:
            if application.application_expiry_email_sent is False:
                log.info(str(datetime.now()) + ' - Sending reminder email: ' + str(application.pk))
                log.info(application.application_id)

                template_id = 'b52414b8-afb4-4b6b-8b10-d87efa2714f4'
                email = UserDetails.objects.get(application_id=application).email
                base_url = settings.PUBLIC_APPLICATION_URL
                email.magic_link_email = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(
                    string.digits)])
                email.magic_link_email = email.magic_link_email.upper()
                log.info(email, base_url, application.token)
                personalisation = {"link": base_url + '/user/validate/' + email.magic_link_email,
                                   "first_name": applicant_name}
                log.info(personalisation['link'])
                r = send_email(email, personalisation, template_id)
                application.application_expiry_email_sent = True
                log.info(r)
                application.save()
                email.save()

        for submission in expired_submissions:

            log.info(str(datetime.now()) + ' - Deleting application: ' + str(submission.pk))

            # Delete Application, with the deletion of associated records handled by on_delete=models.CASCADE in the
            # ForeignKey
            submission.delete()
