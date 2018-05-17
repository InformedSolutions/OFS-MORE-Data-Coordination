import logging
import random
import string
import pytz

from .notify import send_email
from datetime import datetime, timedelta
from .models import AdultInHome, Application, ApplicantPersonalDetails, ApplicantName

from django.conf import settings
from django.shortcuts import reverse

from django_cron import CronJobBase, Schedule


class resend_email(CronJobBase):

    schedule = Schedule(run_every_mins=0.5)
    code = 'application.resend_email'

    def do(self):
        log = logging.getLogger('django.server')
        log.info('Checking for household member health checks not completed in the last 5 days')
        print('Checking for household member health checks not completed in the last 5 days')
        five_days_ago = datetime.now() - timedelta(days=5)
        expired_resends = list(
            AdultInHome.objects.exclude(health_check_status='Done').filter(email_resent__lte=five_days_ago))

        for resend in expired_resends:
            application = Application.objects.get(pk=resend.application_id)
            applicant = ApplicantPersonalDetails.objects.get(application_id=application)
            applicant_name_record = ApplicantName.objects.get(personal_detail_id=applicant)
            if applicant_name_record.middle_names != '':
                applicant_name = applicant_name_record.first_name + ' ' + applicant_name_record.middle_names + ' ' + applicant_name_record.last_name
            elif applicant_name_record.middle_names == '':
                applicant_name = applicant_name_record.first_name + ' ' + applicant_name_record.last_name
            print(str(datetime.now()) + ' - Resending e-mail: ' + str(resend.pk))
            log.info(str(datetime.now()) + ' - Resending e-mail: ' + str(resend.pk))
            template_id = '5bbf3677-49e9-47d0-acf2-55a9a03d8242'
            email = resend.email
            resend.token = ''.join([random.choice(string.digits[1:]) for n in range(7)])
            base_url = settings.PUBLIC_APPLICATION_URL.replace('/childminder', '')
            personalisation = {"link": base_url + reverse('Health-Check-Authentication', kwargs={'id': resend.token}),
                               "firstName": resend.first_name,
                               "ApplicantName": applicant_name}
            print(personalisation['link'])
            r = send_email(email, personalisation, template_id)
            print(r)
            email_resent = resend.email_resent
            if email_resent is not None:
                if email_resent >= 1:
                    resend.email_resent = email_resent + 1
                elif email_resent < 1:
                    resend.email_resent = 1
            else:
                resend.email_resent = 1
            resend.email_resent_timestamp = datetime.now(pytz.utc)
            resend.save()
