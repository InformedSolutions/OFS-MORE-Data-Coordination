import logging

from .models import Application
from .models import ApplicantName
from .models import ApplicantPersonalDetails
from .models import CriminalRecordCheck
from .models import UserDetails
from data_coordinator import settings
from datetime import datetime, timedelta
from application import notify

from django_cron import CronJobBase, Schedule


class delayed_email(CronJobBase):

    RUN_EVERY_MINS = settings.DELAYED_EMAIL_FREQUENCY
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'application.delayed_email'

    def do(self):
        emails = {}
        emails['ofsted_visit_email'] = self.ofsted_visit_emails()
        # to add other types of delayed email then create a def for that email type and append it to the emails array
        log = logging.getLogger('django.server')
        log.info('Checking for delayed emails')
        for email_type in emails:
            for email in emails[email_type]:
                log.info('delayed_email: Sending ' + email_type + ' for Application ID: ' + str(email['application_id']))
                r = notify.send_email(email['email'], email['personalisation'], email['template_id'])
                log.info('delayed_email: response.content = ' + str(r.content))
                if r.status_code == 201:
                    log.info('delayed_email: Sent ' + email_type + ' successfully for Application ID: ' + str(email['application_id']))
                    application = Application.objects.get(application_id=email['application_id'])
                    application.ofsted_visit_email_sent = datetime.now()
                    application.save()
                else:
                    log.warning('delayed_email: Failed Sending ' + email_type + ' successfully for Application ID: ' + str(email['application_id']) + ' - status code:' + str(r.status_code))

    def ofsted_visit_emails(self):
        ove_application_emails = []
        ten_days_ago = datetime.now() - timedelta(days=10)
        completed_applications = Application.objects.filter(application_status='SUBMITTED')
        ofsted_visit_emails_applications = completed_applications.exclude(
            ofsted_visit_email_sent__isnull=False).filter(date_submitted__lte=ten_days_ago)
        for ove_application in ofsted_visit_emails_applications:
            ove_application_email = {}
            ove_application_email['application_id'] = ove_application.application_id
            try:
                conviction = CriminalRecordCheck.objects.get(application_id=ove_application).cautions_convictions
            except CriminalRecordCheck.DoesNotExist:
                conviction = False
            if conviction == False:
                # HEALTH
                ove_application_email['template_id'] = '2cd5f1c5-4900-4922-a627-a0d1f674136b'
            if conviction == True:
                # DBS as well
                ove_application_email['template_id'] = 'c7500574-df3c-4df1-b7f7-8755f6b61c7f'
            first_name = ApplicantName.objects.filter(application_id=ove_application)[:1].get().first_name
            reference = ove_application.application_reference
            ove_application_email['email'] = UserDetails.objects.get(application_id=ove_application).email
            ove_application_email['personalisation'] = {'first_name': first_name, 'ref': reference}
            ove_application_emails.append(ove_application_email)
        return ove_application_emails
