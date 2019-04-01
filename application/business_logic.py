from datetime import datetime, timedelta
from .models import AdultInHome, Application
from application.services.db_gateways import NannyGatewayActions

from django.conf import settings

import logging


def generate_expired_resends():
    """
    Method to return a list of AdultInHome records which are still in To Do status (not Done or Flagged) after an email
    has been sent to them five days ago
    :return: list of AdultInHome records
    """
    five_days_ago = datetime.now() - timedelta(days=5)
    expired_resends = list(
        AdultInHome.objects.exclude(health_check_status='Done').exclude(health_check_status='Flagged').filter(
            email_resent_timestamp__lte=five_days_ago))

    return expired_resends


def find_accepted_applications():
    """
    Method to return a list of accepted applications
    :return: list of Application records
    """
    log = logging.getLogger('django.server')
    time_interval_setting_value = float(settings.NEXT_STEPS_EMAIL_DELAY_IN_DAYS)
    next_steps_send_email_threshold = datetime.now() - timedelta(days=time_interval_setting_value)
    log.info(time_interval_setting_value)
    log.info(next_steps_send_email_threshold)

    send_next_steps = list(
        Application.objects.filter(application_status='ACCEPTED',
                                   date_accepted__lte=next_steps_send_email_threshold,
                                   ofsted_visit_email_sent=None
                                   )
    )
    return send_next_steps


def generate_expiring_applications_list_cm_applications():

    '''Method to return a list of childminder applications that have not been accessed in the last 55 days'''

    due_expiry_email = datetime.now() - timedelta(days=settings.WARNING_EMAIL_THRESHOLD)
    expiring_applications = list(
        Application.objects.filter(application_status='DRAFTING', date_last_accessed=due_expiry_email)
    )
    return expiring_applications


def generate_expiring_applications_list_nanny_applications():

    '''Method to return a list of nanny applications that have not been accessed in the last 55 days'''

    due_expiry_email = datetime.now() - timedelta(days=settings.WARNING_EMAIL_THRESHOLD)
    expiring_applications = list(
                                NannyGatewayActions().list('nanny_application',
                                                           params={"application_status": 'DRAFTING',
                                                                   "date_last_accessed": due_expiry_email})
    )
    return expiring_applications


def generate_list_of_expired_cm_applications():
    expiry_threshold = datetime.now() - timedelta(days=settings.CHILDMINDER_EXPIRY_THRESHOLD)
        # Determine expired applications based on date last accessed
    expired_submissions_cm = list(
            Application.objects.filter(application_status='DRAFTING', date_last_accessed=expiry_threshold))

    return expired_submissions_cm


def generate_list_of_expired_nanny_applications():
    expiry_threshold = datetime.now() - timedelta(days=settings.NANNY_EXPIRY_THRESHOLD)
    expired_submissions_nanny = list(
            NannyGatewayActions().list('nanny_application',
                                       params={"application_status": 'DRAFTING',
                                               "date_last_accessed": expiry_threshold}))

    return expired_submissions_nanny
