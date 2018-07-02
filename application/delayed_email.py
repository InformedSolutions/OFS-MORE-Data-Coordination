import logging

from .notify import send_email
from datetime import datetime
from .models import Application, ApplicantPersonalDetails, ApplicantName, UserDetails
from .business_logic import find_accepted_applications

from django.conf import settings
from django_cron import CronJobBase, Schedule


class delayed_email(CronJobBase):

    schedule = Schedule(run_every_mins=1)
    code = 'application.delayed_email'

    def do(self):
        """
        Function for sending a reminder email detailing next steps to an applicant
        """
        log = logging.getLogger('django.server')
        log.info('Checking for applications that have been accepted 10 days ago')
        send_next_steps = find_accepted_applications()
        log.info(send_next_steps)

        for send in send_next_steps:
            application = Application.objects.get(pk=send.application_id)
            log.info(application)

            if ApplicantPersonalDetails.objects.filter(application_id=application).count() > 0:
                applicant = ApplicantPersonalDetails.objects.get(application_id=application)
                applicant_name_record = ApplicantName.objects.get(personal_detail_id=applicant)
                log.info(applicant_name_record)
                applicant_name = applicant_name_record.first_name
            else:
                applicant_name = 'applicant'

            log.info(applicant_name)
            log.info(str(datetime.now()) + ' - Sending next steps: ' + str(send.pk))
            template_id = '3de3b404-64fc-49a1-b01f-1d0607760c60'
            email = UserDetails.objects.get(application_id=application).email
            log.info(email)
            base_url = settings.PUBLIC_APPLICATION_URL
            log.info(base_url)
            documents_needed = base_url + '/documents-needed?id=' + str(send.application_id)
            log.info(documents_needed)
            home_ready = base_url + '/home-ready?id=' + str(send.application_id)
            prepare_interview = base_url + '/prepare-interview?id=' + str(send.application_id)
            personalisation = {"ref": str(send.application_reference),
                               "first_name": applicant_name,
                               "documents_needed": documents_needed,
                               "home_ready": home_ready,
                               "prepare_interview": prepare_interview}

            log.info(personalisation)
            r = send_email(email, personalisation, template_id)
            log.info(r)
            send.ofsted_visit_email_sent = datetime.now()
            send.save()
            log.info(send.ofsted_visit_email_sent)
