from django.test import TestCase

from ..resend_email import *

class DataCoordinatorTests(TestCase):

    # Create your tests here.
    def test_resend_email(self):
        resend_email_job = resend_email()
        resend_email_job.do()

