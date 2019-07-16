from datetime import datetime, timedelta
from .models import AdultInHome, Application

from django.conf import settings

import logging


log = logging.getLogger(__name__)


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
    """
    Method to return a list of childminder applications that have not been accessed in the last 55 days
    """

    threshold_datetime = datetime.now() - timedelta(days=settings.WARNING_EMAIL_THRESHOLD_DAYS)
    log.debug('childminder drafts not accessed for {} days (before {})'.format(settings.WARNING_EMAIL_THRESHOLD_DAYS,
                                                                               threshold_datetime))
    expiring_applications = list(
        Application.objects.filter(application_status='DRAFTING', date_last_accessed__lt=threshold_datetime)
    )
    log.debug('found {}'.format(len(expiring_applications)))
    return expiring_applications


def generate_list_of_expired_cm_applications():
    expiry_threshold = datetime.now() - timedelta(days=settings.CHILDMINDER_EXPIRY_THRESHOLD)
    log.debug('childminder drafts not accessed for {} days (before {})'.format(
        settings.CHILDMINDER_EXPIRY_THRESHOLD, expiry_threshold))
    # Determine expired applications based on date last accessed
    expired_submissions_cm = list(Application.objects.filter(application_status='DRAFTING',
                                                             date_last_accessed__lt=expiry_threshold))

    log.debug('found {}'.format(len(expired_submissions_cm)))
    return expired_submissions_cm