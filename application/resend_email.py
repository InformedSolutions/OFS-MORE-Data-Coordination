import logging
import random
import string
import pytz

from .notify import send_email
from datetime import datetime, timedelta
from .models import AdultInHome, Application, ApplicantPersonalDetails, ApplicantName
from .business_logic import generate_expired_resends

from django.conf import settings
from django_cron import CronJobBase, Schedule


class resend_email(CronJobBase):

    schedule = Schedule(run_every_mins=1)
    code = 'application.resend_email'

    def do(self):
        log = logging.getLogger('django.server')
        log.info('Checking for household member health checks not completed in the last 5 days')
        expired_resends = generate_expired_resends()
        log.info(expired_resends)
        # For each adult record, resend the household member health check email
        for resend in expired_resends:
            application = Application.objects.get(pk=resend.application_id.application_id)
            log.info(application)
            applicant = ApplicantPersonalDetails.objects.get(application_id=application)
            applicant_name_record = ApplicantName.objects.get(personal_detail_id=applicant)
            log.info(applicant_name_record)
            if applicant_name_record.middle_names != '':
                applicant_name = applicant_name_record.first_name + ' ' + applicant_name_record.middle_names + ' ' + applicant_name_record.last_name
            elif applicant_name_record.middle_names == '':
                applicant_name = applicant_name_record.first_name + ' ' + applicant_name_record.last_name
            log.info(applicant_name)
            log.info(str(datetime.now()) + ' - Resending e-mail: ' + str(resend.pk))
            template_id = '5bbf3677-49e9-47d0-acf2-55a9a03d8242'
            email = resend.email
            log.info(email)
            resend.token = ''.join([random.choice(string.digits[1:]) for n in range(7)])
            log.info(resend.token)
            base_url = settings.PUBLIC_APPLICATION_URL
            log.info(base_url)
            personalisation = {"link": base_url + '/health-check/' + resend.token,
                               "firstName": resend.first_name,
                               "ApplicantName": applicant_name}
            log.info(personalisation['link'])
            r = send_email(email, personalisation, template_id)
            log.info(r)
            # Increase the email resend count by 1
            email_resent = resend.email_resent
            if email_resent is not None:
                resend.email_resent = email_resent + 1
            else:
                resend.email_resent = 1
            resend.email_resent_timestamp = datetime.now(pytz.utc)
            resend.save()
            log.info(resend.email_resent_timestamp)
