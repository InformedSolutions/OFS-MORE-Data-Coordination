from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from .models import AdultInHome, Application
from application.services.db_gateways import NannyGatewayActions, HMGatewayActions

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
    log.debug('childminder drafts not accessed for {} days (before {})'.format(settings.WARNING_EMAIL_THRESHOLD_DAYS,
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
    log.debug('nanny drafts not accessed for {} days (before {})'.format(settings.WARNING_EMAIL_THRESHOLD_DAYS,
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
    expiry_threshold = datetime.now() - timedelta(days=settings.CHILDMINDER_EXPIRY_THRESHOLD)
    log.debug('childminder drafts not accessed for {} days (before {})'.format(
        settings.CHILDMINDER_EXPIRY_THRESHOLD, expiry_threshold))
    # Determine expired applications based on date last accessed
    expired_submissions_cm = list(Application.objects.filter(application_status='DRAFTING',
                                                             date_last_accessed__lt=expiry_threshold))

    log.debug('found {}'.format(len(expired_submissions_cm)))
    return expired_submissions_cm


def generate_list_of_expired_nanny_applications():
    expiry_threshold = datetime.now() - timedelta(days=settings.NANNY_EXPIRY_THRESHOLD)
    log.debug('nanny drafts not accessed for {} days (before {})'.format(settings.NANNY_EXPIRY_THRESHOLD,
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


def generate_list_of_adults_not_completed_health_check(no_days):
    """
    function to list any adults who haven't completed the household members health check
    after x days
    :param no_days: the number of days which is the threshold for the reminder email
    :return: list of adult records
    """
    now = datetime.today()
    adults_to_remind = []
    response = HMGatewayActions().list('adult',
                                          params={"adult_status": 'WAITING', 'health_check_status': 'To do', })
    if no_days == settings.SECOND_HEALTH_CHECK_REMINDER_THRESHOLD:
        sent_field = 'second_health_check_reminder_sent'
    elif no_days == settings.THIRD_HEALTH_CHECK_REMINDER_THRESHOLD:
        sent_field = 'third_health_check_reminder_sent'
    else:
        return adults_to_remind

    if response.status_code == 200:
        adults_waiting = response.record
        for adult in adults_waiting:
            email_sent = datetime.strptime(adult['email_resent_timestamp'][:19], '%Y-%m-%dT%H:%M:%S')
            no_days = float(no_days)
            no_days_timedelta = timedelta(days=no_days)
            if (now - email_sent) >= no_days_timedelta and not adult[sent_field]:
                adults_to_remind.append(adult)
    elif response.status_code == 404:
        adults_to_remind = []
    else:
        raise ConnectionError(response.status_code)

    log.debug('found {}'.format(len(adults_to_remind)))

    return adults_to_remind

def extract_applications_in_queue():
    """
    function to list any application that has a status of SUBMITTED, grouped by date and by application.
    :return: list of adult, childminder and nanny records
    """
    now = datetime.now()
    initial_date = datetime(2020, 2, 19, 0, 0)
    delta = timedelta(days=1)
    adult_response = HMGatewayActions().list('adult', params={"adult_status": 'SUBMITTED'})
    nanny_response = NannyGatewayActions().list('application', params={"application_status": 'SUBMITTED'})
    cm_applications = list(Application.objects.filter(application_status='SUBMITTED',))
    apps_in_queue = {}
    while initial_date <= now:
        cm_apps = 0
        adult_apps = 0
        nanny_apps = 0
        for item in cm_applications:
            if item.date_submitted == initial_date:
                cm_apps += 1
        if adult_response.status_code == 200:
            adults_submitted = adult_response.record
            for adult in adults_submitted:
                if adult.date_resubmitted is None and adult.date_submitted == initial_date:
                    adult_apps += 1
                elif adult.date_resubmitted == initial_date:
                    adult_apps += 1
        if nanny_response.status_code == 200:
            nannies_submitted = nanny_response.record
            for nanny in nannies_submitted:
                if nanny.date_submitted == initial_date:
                    nanny_apps += 1

        apps_in_queue[initial_date]['Childminder'] = cm_apps
        apps_in_queue[initial_date]['Adults'] = adult_apps
        apps_in_queue[initial_date]['Nanny'] = nanny_apps
        initial_date += delta

    return (apps_in_queue)



