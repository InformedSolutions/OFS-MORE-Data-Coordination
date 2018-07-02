from datetime import datetime, timedelta
from .models import AdultInHome, Application

from django.conf import settings


def generate_expired_resends():
    """
    Method to return a list of AdultInHome records which are still in To Do status after an email has been sent to them
    five days ago
    :return: list of AdultInHome records
    """
    five_days_ago = datetime.now() - timedelta(days=5)
    expired_resends = list(
        AdultInHome.objects.exclude(health_check_status='Done').filter(email_resent_timestamp__lte=five_days_ago))

    return expired_resends


def find_accepted_applications():
    """
    Method to return a list of accepted applications
    :return: list of Application records
    """
    time_interval_setting_value = int(settings.NEXT_STEPS_EMAIL_DELAY_IN_DAYS)
    next_steps_send_email_threshold = datetime.now() - timedelta(days=time_interval_setting_value)
    send_next_steps = list(
        Application.objects.filter(application_status='ACCEPTED',
                                   date_accepted__lte=next_steps_send_email_threshold
                                   )
    )

    return send_next_steps
