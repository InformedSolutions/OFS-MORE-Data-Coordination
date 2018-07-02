from datetime import datetime, timedelta
from .models import AdultInHome


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
