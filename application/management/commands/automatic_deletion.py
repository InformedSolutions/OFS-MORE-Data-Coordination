

from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from application import models


class Command(BaseCommand):
    help = 'Delete all records that are over 90 days old'

    def handle(self, *args, **options):
        ninety_days_ago = datetime.now() - timedelta(days=90)

        test_model = list(models.Application.objects.filter(date_updated__lte=ninety_days_ago))
        for model in test_model:

            model.delete()
            self.stdout.write((str(datetime.now()) + ' - Deleted application: ' + str(model.pk)))
