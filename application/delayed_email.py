import logging

from .notify import send_email
from datetime import datetime, timedelta
from .models import Application, ApplicantPersonalDetails, ApplicantName

from django.conf import settings
from django_cron import CronJobBase, Schedule


class delayed_email(CronJobBase):

    schedule = Schedule(run_every_mins=1)
    code = 'application.delayed_email'

    def do(self):
        log = logging.getLogger('django.server')
        log.info('Checking for applications that have been submitted 10 days ago')
        ten_days_ago = datetime.now() - timedelta(days=10)
        log.info(ten_days_ago)
        send_next_steps = list(
            Application.objects.filter(application_status='SUBMITTED', ofsted_visit_email_sent__lte=ten_days_ago))
        log.info(send_next_steps)
        for send in send_next_steps:
            application = Application.objects.get(pk=send.application_id.application_id)
            log.info(application)
            if ApplicantPersonalDetails.objects.filter(application_id=application).count() > 0:
                applicant = ApplicantPersonalDetails.objects.get(application_id=application)
                applicant_name_record = ApplicantName.objects.get(personal_detail_id=applicant)
                log.info(applicant_name_record)
                applicant_name = applicant_name_record.first_name
            log.info(applicant_name)
            log.info(str(datetime.now()) + ' - Sending next steps: ' + str(send.pk))
            template_id = '3de3b404-64fc-49a1-b01f-1d0607760c60'
            email = send.email
            log.info(email)
            base_url = settings.PUBLIC_APPLICATION_URL
            log.info(base_url)
            personalisation = {"documents-needed": base_url + '/documents-needed?id=' + send.application_id,
                               "home-ready": base_url + '/home-ready?id=' + send.application_id,
                               "prepare-interview": base_url + '/prepare-interview?id=' + send.application_id,
                               "firstName": send.first_name,
                               "ref": send.application_reference}
            r = send_email(email, personalisation, template_id)
            log.info(r)
            send.ofsted_visit_email_sent = datetime.now()
            send.save()
            log.info(send.ofsted_visit_email_sent)

