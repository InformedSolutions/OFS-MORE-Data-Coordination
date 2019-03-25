from datetime import datetime, timedelta
from django.test import TestCase
from uuid import UUID

from ..business_logic import generate_expired_resends, find_accepted_applications, generate_expiring_applications_list
from ..models import AdultInHome, Application, UserDetails
from ..resend_email import *


class DataCoordinatorTests(TestCase):

    def test_resend_email_expired(self):
        """
        Test to check health check email resend logic if there are expired health checks
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
        user_record = UserDetails.objects.create(
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
        adult_record = AdultInHome.objects.create(
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
        test_adult_id_2 = '166f77f7-c2ee-4550-9461-45b9d2f28d33'
        adult_record_2 = AdultInHome.objects.create(
            adult_id=(UUID(test_adult_id_2)),
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
            health_check_status='Done',
            email_resent=0,
            email_resent_timestamp=datetime.now(pytz.utc) - timedelta(10)
        )
        test_adult_id_3 = '166f77f7-c2ee-4550-9461-45b9d2f28d32'
        adult_record_3 = AdultInHome.objects.create(
            adult_id=(UUID(test_adult_id_3)),
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
            health_check_status='Flagged',
            email_resent=0,
            email_resent_timestamp=datetime.now(pytz.utc) - timedelta(10)
        )
        expired_resends = generate_expired_resends()
        assert (len(expired_resends) == 1)
        application.delete()
        user_record.delete()
        adult_record.delete()
        adult_record_2.delete()
        adult_record_3.delete()

    def test_resend_email_not_expired(self):
        """
        Test to check health check email resend logic if there are no expired health checks
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
        user_record = UserDetails.objects.create(
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
        adult_record = AdultInHome.objects.create(
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
            email_resent_timestamp=datetime.now(pytz.utc)
        )
        expired_resends = generate_expired_resends()
        assert (len(expired_resends) == 0)
        application.delete()
        user_record.delete()
        adult_record.delete()

    def test_find_accepted_applications(self):
        """
        Test to check find accepted applications logic
        """
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        test_application_id_2 = 'f8c42666-1367-4878-92e2-1cee6ebcb48b'
        application = Application.objects.create(
            application_id=(UUID(test_application_id)),
            application_type='CHILDMINDER',
            application_status='ACCEPTED',
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
            declarations_status='COMPLETED',
            date_created=datetime.today(),
            date_updated=datetime.today(),
            date_accepted=datetime.today() - timedelta(11)
        )
        application2 = Application.objects.create(
            application_id=(UUID(test_application_id_2)),
            application_type='CHILDMINDER',
            application_status='ACCEPTED',
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
            declarations_status='COMPLETED',
            date_created=datetime.today(),
            date_updated=datetime.today(),
            date_accepted=datetime.today()
        )
        send_next_steps = find_accepted_applications()
        assert (len(send_next_steps) == 1)
        application.delete()
        application2.delete()

    def test_whether_reminder_email_is_sent_when_email_not_sent_previously(self):
        """
        Test to check logic for reminder email for 55 days inactivity when the email has already been sent to the applicant in the past
        """
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
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
            date_last_accessed=datetime.now() - timedelta(days=55),
            application_expiry_email_sent=False
        )
        user_record = UserDetails.objects.create(
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

        expiring_applications = generate_expiring_applications_list()
        assert (len(expiring_applications) == 1)
        application.delete()
        user_record.delete()

    def test_whether_reminder_email_is_sent_when_email_already_sent_previously(self):
        """
        Test to check logic for reminder email for 55 days inactivity when applicant has already recieved this email
        """
        test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
        test_login_id = '004551ca-21fa-4dbe-9095-0384e73b3cbe'
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
            date_last_accessed=datetime.now() - timedelta(days=55),
            application_expiry_email_sent=True
        )
        user_record = UserDetails.objects.create(
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

        expiring_applications = generate_expiring_applications_list()
        assert (len(expiring_applications) == 0)
        application.delete()
        user_record.delete()
