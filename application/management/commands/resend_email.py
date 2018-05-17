import random
import string
import pytz

from application.notify import send_email
from application.models import AdultInHome, Application, ApplicantPersonalDetails, ApplicantName

from django.conf import settings
from django.shortcuts import reverse

from datetime import datetime, timedelta
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Resend e-mails for household member health checks not touched in the last 5 days'

    def handle(self, *args, **options):
        five_days_ago = datetime.now() - timedelta(days=5)

        test_model = list(AdultInHome.objects.filter(date_updated__lte=five_days_ago))
        for model in test_model:
            application = Application.objects.get(pk=model.application_id)
            applicant = ApplicantPersonalDetails.objects.get(application_id=application)
            applicant_name_record = ApplicantName.objects.get(personal_detail_id=applicant)
            if applicant_name_record.middle_names != '':
                applicant_name = applicant_name_record.first_name + ' ' + applicant_name_record.middle_names + ' ' + applicant_name_record.last_name
            elif applicant_name_record.middle_names == '':
                applicant_name = applicant_name_record.first_name + ' ' + applicant_name_record.last_name
            print(str(datetime.now()) + ' - Resending e-mail: ' + str(model.pk))
            template_id = '5bbf3677-49e9-47d0-acf2-55a9a03d8242'
            email = model.email
            model.token = ''.join([random.choice(string.digits[1:]) for n in range(7)])
            base_url = settings.PUBLIC_APPLICATION_URL.replace('/childminder', '')
            personalisation = {"link": base_url + reverse('Health-Check-Authentication', kwargs={'id': model.token}),
                               "firstName": model.first_name,
                               "ApplicantName": applicant_name}
            print(personalisation['link'])
            r = send_email(email, personalisation, template_id)
            print(r)
            email_resent = model.email_resent
            if email_resent is not None:
                if email_resent >= 1:
                    model.email_resent = email_resent + 1
                elif email_resent < 1:
                    model.email_resent = 1
            else:
                model.email_resent = 1
            model.email_resent_timestamp = datetime.now(pytz.utc)
            model.save()
            self.stdout.write((str(datetime.now()) + ' - Deleted application: ' + str(model.pk)))
