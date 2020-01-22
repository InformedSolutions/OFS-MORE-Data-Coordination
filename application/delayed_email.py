import logging

from .notify import send_email
from datetime import datetime
from .models import Application, ApplicantPersonalDetails, ApplicantName, UserDetails, ChildcareType
from .business_logic import find_accepted_applications
from . import utils

from django.conf import settings
from django_cron import CronJobBase, Schedule


log = logging.getLogger(__name__)


class DelayedEmail(CronJobBase):

    schedule = Schedule(run_every_mins=settings.SEND_EMAIL_POLL_MINS)
    code = 'application.delayed_email'

    def do(self):
        """
        Function for sending a reminder email detailing next steps to an applicant
        """
        with utils.CronErrorContext():
            log.info('Checking for applications that have been accepted x days ago')
            send_next_steps = find_accepted_applications()
            log.info(send_next_steps)

            for send in send_next_steps:
                with utils.CronErrorContext():
                    application = Application.objects.get(pk=send.application_id)
                    log.info('Application ID: ' + str(application.application_id))

                    applicant = ApplicantPersonalDetails.objects.get(application_id=application)
                    applicant_name_record = ApplicantName.objects.get(personal_detail_id=applicant)
                    applicant_name = applicant_name_record.first_name

                    childcare_type_record = ChildcareType.objects.get(application_id=application)

                    # Only send What you need for Ofsted's visit e-mail if the applicant is not applying to
                    # the Childcare Register
                    if childcare_type_record.zero_to_five:

                        log.info(str(datetime.now()) + ' - Sending next steps: ' + str(send.pk))
                        template_id = '3de3b404-64fc-49a1-b01f-1d0607760c60'
                        email = UserDetails.objects.get(application_id=application).email
                        log.info(email)
                        base_url = settings.CHILDMINDER_EMAIL_VALIDATION_URL
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
                        if r.status_code not in (200, 201):
                            raise ConnectionError(r.status_code)
                        send.ofsted_visit_email_sent = datetime.now()
                        send.save()
                        log.info("Sending What you need for Ofsted's visit email")
                        log.info(send.ofsted_visit_email_sent)
                    else:
                        log.info("Not sending What you need for Ofsted's visit email")

