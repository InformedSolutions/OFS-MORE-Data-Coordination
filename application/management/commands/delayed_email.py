from application.notify import send_email
from application.models import AdultInHome, Application, ApplicantPersonalDetails, ApplicantName

from django.conf import settings

from datetime import datetime, timedelta
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Send e-mail with next steps 10 days after the application has been submitted'

    def handle(self, *args, **options):
        ten_days_ago = datetime.now() - timedelta(days=10)

        test_model = list(
            Application.objects.filter(application_status='SUBMITTED', ofsted_visit_email_sent=ten_days_ago))
        for model in test_model:
            application = Application.objects.get(pk=model.application_id)
            applicant = ApplicantPersonalDetails.objects.get(application_id=application)
            applicant_name_record = ApplicantName.objects.get(personal_detail_id=applicant)
            applicant_name = applicant_name_record.first_name
            print(str(datetime.now()) + ' - Sending e-mail: ' + str(model.pk))
            template_id = '3de3b404-64fc-49a1-b01f-1d0607760c60'
            email = model.email
            base_url = settings.PUBLIC_APPLICATION_URL.replace('/childminder', '')
            documents_needed = base_url + '/documents-needed?id=' + str(model.application_id)
            home_ready = base_url + '/home-ready?id=' + str(model.application_id)
            prepare_interview = base_url + '/prepare-interview?id=' + str(model.application_id)
            personalisation = {"ref": str(model.application_reference),
                               "first_name": applicant_name,
                               "documents_needed": documents_needed,
                               "home_ready": home_ready,
                               "prepare_interview": prepare_interview}
            r = send_email(email, personalisation, template_id)
            print(r)
            model.ofsted_visit_email_sent = datetime.now()
            model.save()
            self.stdout.write((str(datetime.now()) + ' - Deleted application: ' + str(model.pk)))
