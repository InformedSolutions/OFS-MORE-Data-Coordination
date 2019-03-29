from datetime import datetime, timedelta
from .models import AdultInHome, Application
from application.services.db_gateways import NannyGatewayActions

from django.conf import settings

import logging


log = logging.getLogger(__name__)


def generate_expired_resends():
    """
    Method to return a list of AdultInHome records which are still in To Do status (not Done or Flagged) after an email
    has been sent to them x days ago
    :return: list of AdultInHome records
    """
    days = 5
    x_days_ago = datetime.now() - timedelta(days=days)
    log.debug('health check adults not reminded in last {} days (before {})'.format(days, x_days_ago))
    expired_resends = list(
        AdultInHome.objects.exclude(health_check_status='Done').exclude(health_check_status='Flagged').filter(
            email_resent_timestamp__lte=x_days_ago))
    log.debug('found {}'.format(len(expired_resends)))
    return expired_resends


def find_accepted_applications():
    """
    Method to return a list of accepted applications
    :return: list of Application records
    """
    time_interval_setting_value = float(settings.NEXT_STEPS_EMAIL_DELAY_IN_DAYS)
    next_steps_send_email_threshold = datetime.now() - timedelta(days=time_interval_setting_value)
    log.debug('childminders accepted {} days ago (before {})'.format(settings.NEXT_STEPS_EMAIL_DELAY_IN_DAYS,
                                                                     next_steps_send_email_threshold))
    send_next_steps = list(
        Application.objects.filter(application_status='ACCEPTED',
                                   date_accepted__lte=next_steps_send_email_threshold,
                                   ofsted_visit_email_sent=None)
    )
    log.debug('found {}'.format(len(send_next_steps)))
    return send_next_steps


def generate_expiring_applications_list_cm_applications():
    """
    Method to return a list of childminder applications that have not been accessed in the last 55 days
    """

    threshold_datetime = datetime.now() - timedelta(days=settings.WARNING_EMAIL_THRESHOLD_DAYS)
    log.debug('childminders not accessed in {} days (before {})'.format(settings.WARNING_EMAIL_THRESHOLD_DAYS,
                                                                        threshold_datetime))
    expiring_applications = list(
        Application.objects.filter(application_status='DRAFTING', date_last_accessed__lt=threshold_datetime)
    )
    log.debug('found {}'.format(len(expiring_applications)))
    return expiring_applications


def generate_expiring_applications_list_nanny_applications():
    """
    Method to return a list of nanny applications that have not been accessed in the last 55 days
    """

    threshold_datetime = datetime.now() - timedelta(days=settings.WARNING_EMAIL_THRESHOLD_DAYS)
    log.debug('nannies not accessed in {} days (before {})'.format(settings.WARNING_EMAIL_THRESHOLD_DAYS,
                                                                   threshold_datetime))
    response = NannyGatewayActions().list('application',
                                          params={"application_status": 'DRAFTING',
                                                  "last_accessed_before": threshold_datetime.isoformat()})
    if response.status_code == 200:
        expiring_applications = response.record
    elif response.status_code == 404:
        expiring_applications = []
    else:
        raise ConnectionError(response.status_code)

    log.debug('found {}'.format(len(expiring_applications)))
    return expiring_applications


def generate_list_of_expired_cm_applications():
    expiry_threshold = datetime.now() - timedelta(days=settings.APPLICATION_EXPIRY_THRESHOLD_DAYS)
    log.debug('childminders not accessed in {} days (before {})'.format(settings.APPLICATION_EXPIRY_THRESHOLD_DAYS,
                                                                        expiry_threshold))
    # Determine expired applications based on date last accessed
    expired_submissions_cm = list(Application.objects.filter(application_status='DRAFTING',
                                                             date_last_accessed__lt=expiry_threshold))

    log.debug('found {}'.format(len(expired_submissions_cm)))
    return expired_submissions_cm


def generate_list_of_expired_nanny_applications():
    expiry_threshold = datetime.now() - timedelta(days=settings.APPLICATION_EXPIRY_THRESHOLD_DAYS)
    log.debug('nannies not accessed in {} days (before {})'.format(settings.APPLICATION_EXPIRY_THRESHOLD_DAYS,
                                                                   expiry_threshold))
    response = NannyGatewayActions().list('application',
                                          params={"application_status": 'DRAFTING',
                                                  "last_accessed_before": expiry_threshold.isoformat()})
    if response.status_code == 200:
        expired_submissions_nanny = response.record
    elif response.status_code == 404:
        expired_submissions_nanny = []
    else:
        raise ConnectionError(response.status_code)

    log.debug('found {}'.format(len(expired_submissions_nanny)))

    return expired_submissions_nanny


