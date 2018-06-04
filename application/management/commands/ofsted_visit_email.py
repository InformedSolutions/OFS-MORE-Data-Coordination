

from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from application import models


class Command(BaseCommand):
    help = 'Send email after n amount of days'

    def handle(self, *args, **options):
        ten_days_ago = datetime.now() - timedelta(days=10)

        test_model = list(models.Application.objects.filter(date_updated__lte=ten_days_ago))
        for model in test_model:
            print('send email after n amount of days')
