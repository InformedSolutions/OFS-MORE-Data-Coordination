from django.test import TestCase
from uuid import UUID

from ..business_logic import generate_expired_resends
from ..models import AdultInHome, Application, UserDetails
from ..resend_email import *


class DataCoordinatorTests(TestCase):

    def test_resend_email(self):
        """
        Test to check if health check email gets resent automatically after more than 5 days if the health check has
        not yet been completed
        """
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
        AdultInHome.objects.filter(application_id=test_application_id, adult=1).delete()
        UserDetails.objects.filter(login_id=test_login_id).delete()
        application = Application.objects.create(
            application_id=(UUID(test_application_id)),
            application_type='CHILDMINDER',
            application_status='DRAFTING',
            cygnum_urn='',
            login_details_status='COMPLETED',
            personal_details_status='NOT_STARTED',
            childcare_type_status='COMPLETED',
            first_aid_training_status='COMPLETED',
            eyfs_training_status='COMPLETED',
            criminal_record_check_status='COMPLETED',
            health_status='COMPLETED',
            references_status='COMPLETED',
            people_in_home_status='COMPLETED',
            declarations_status='NOT_STARTED',
            date_created=datetime.today(),
            date_updated=datetime.today(),
            date_accepted=None,
        )
        UserDetails.objects.create(
            login_id=(UUID(test_login_id)),
            application_id=application,
            email='',
            mobile_number='',
            add_phone_number='',
            email_expiry_date=None,
            sms_expiry_date=None,
            magic_link_email='',
            magic_link_sms=''
        )
        test_adult_id = '166f77f7-c2ee-4550-9461-45b9d2f28d34'
        AdultInHome.objects.create(
            adult_id=(UUID(test_adult_id)),
            application_id=application,
            adult=1,
            first_name='',
            middle_names='',
            last_name='',
            birth_day=0,
            birth_month=0,
            birth_year=0,
            relationship='',
            dbs_certificate_number=0,
            health_check_status='To do',
            email_resent=0,
            email_resent_timestamp=datetime.now(pytz.utc) - timedelta(10)
        )
        expired_resends = generate_expired_resends()
        assert (len(expired_resends) == 1)
