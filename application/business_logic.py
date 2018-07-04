from datetime import datetime, timedelta
from .models import AdultInHome, Application

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
    #time_interval_setting_value = int(settings.NEXT_STEPS_EMAIL_DELAY_IN_DAYS)
    #next_steps_send_email_threshold = datetime.now() - timedelta(days=time_interval_setting_value)
    next_steps_send_email_threshold = datetime.now() - timedelta(minutes=1)

    #log = logging.getLogger('django.server')
    #log.info('Time logging interval:' + str(time_interval_setting_value))
    #log.info('Next steps send email threshold:' + str(next_steps_send_email_threshold))
    send_next_steps = list(
        Application.objects.filter(application_status='ACCEPTED',
                                   date_accepted__lte=next_steps_send_email_threshold
                                   )
    )

    return send_next_steps
