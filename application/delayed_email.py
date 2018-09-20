import logging

from .notify import send_email
from datetime import datetime
from .models import Application, ApplicantPersonalDetails, ApplicantName, UserDetails, ChildcareType
from .business_logic import find_accepted_applications

from django.conf import settings
from django_cron import CronJobBase, Schedule


class DelayedEmail(CronJobBase):

    schedule = Schedule(run_every_mins=1)
    code = 'application.delayed_email'

    def do(self):
        """
        Function for sending a reminder email detailing next steps to an applicant
        """
        try:
            log = logging.getLogger('django.server')
            log.info('Checking for applications that have been accepted 10 days ago')
            send_next_steps = find_accepted_applications()
            log.info(send_next_steps)

            for send in send_next_steps:
                application = Application.objects.get(pk=send.application_id)
                log.info(application.application_id)

                applicant = ApplicantPersonalDetails.objects.get(application_id=application)
                applicant_name_record = ApplicantName.objects.get(personal_detail_id=applicant)
                log.info(applicant_name_record)
                applicant_name = applicant_name_record.first_name
                log.info(applicant_name)

                childcare_type_record = ChildcareType.objects.get(application_id=application)
                log.info(childcare_type_record)

                # Only send What you need for Ofsted's visit e-mail if the applicant is not applying to the Childcare
                # Register
                if childcare_type_record.zero_to_five is True:

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

                    r = send_email(email, personalisation, template_id)
                    log.info(r)
                    send.ofsted_visit_email_sent = datetime.now()
                    send.save()
                    log.info(send.ofsted_visit_email_sent)
        except Exception as e:
            log.info(e)
