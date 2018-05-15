"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- models.py --

@author: Informed Solutions
"""
from datetime import datetime
from uuid import uuid4

from django.db import models

TASK_STATUS = (
    ('NOT_STARTED', 'NOT_STARTED'),
    ('FLAGGED', 'FLAGGED'),
    ('COMPLETE', 'COMPLETE')
)


class ArcComments(models.Model):
    """
    Model for ARC_COMMENTS table.
    """
    review_id = models.UUIDField(primary_key=True, default=uuid4, unique=True),
    table_pk = models.UUIDField(blank=True)
    table_name = models.CharField(max_length=30, blank=True)
    field_name = models.CharField(max_length=40, blank=True)
    comment = models.CharField(max_length=100, blank=True)
    flagged = models.BooleanField()

    @classmethod
    def get_id(cls, app_id):
        return cls.objects.get(application_id=app_id)

    class Meta:
        db_table = 'ARC_COMMENTS'


class Arc(models.Model):
    """
    Model for the ARC table.
    """
    application_id = models.UUIDField(primary_key=True, default=uuid4)
    user_id = models.CharField(max_length=50, blank=True)
    last_accessed = models.CharField(max_length=50)
    app_type = models.CharField(max_length=50)
    # What was previously ArcStatus is below
    login_details_review = models.CharField(choices=TASK_STATUS, max_length=50, default='NOT_STARTED')
    childcare_type_review = models.CharField(choices=TASK_STATUS, max_length=50, default='NOT_STARTED')
    personal_details_review = models.CharField(choices=TASK_STATUS, max_length=50, default='NOT_STARTED')
    first_aid_review = models.CharField(choices=TASK_STATUS, max_length=50, default='NOT_STARTED')
    eyfs_review = models.CharField(choices=TASK_STATUS, max_length=50, default='NOT_STARTED')
    dbs_review = models.CharField(choices=TASK_STATUS, max_length=50, default='NOT_STARTED')
    health_review = models.CharField(choices=TASK_STATUS, max_length=50, default='NOT_STARTED')
    references_review = models.CharField(choices=TASK_STATUS, max_length=50, default='NOT_STARTED')
    people_in_home_review = models.CharField(choices=TASK_STATUS, max_length=50, default='NOT_STARTED')

    @classmethod
    def get_id(cls, app_id):
        return cls.objects.get(application_id=app_id)

    class Meta:
        db_table = 'ARC'


class Application(models.Model):
    """
    Model for APPLICATION table
    """
    APP_STATUS = (
        ('ARC_REVIEW', 'ARC_REVIEW'),
        ('CANCELLED', 'CANCELLED'),
        ('CYGNUM_REVIEW', 'CYGNUM_REVIEW'),
        ('DRAFTING', 'DRAFTING'),
        ('FURTHER_INFORMATION', 'FURTHER_INFORMATION'),
        ('NOT_REGISTERED', 'NOT_REGISTERED'),
        ('REGISTERED', 'REGISTERED'),
        ('REJECTED', 'REJECTED'),
        ('SUBMITTED', 'SUBMITTED'),
        ('WITHDRAWN', 'WITHDRAWN')
    )
    APP_TYPE = (
        ('CHILDMINDER', 'CHILDMINDER'),
        ('NANNY', 'NANNY'),
        ('NURSERY', 'NURSERY'),
        ('SOCIAL_CARE', 'SOCIAL_CARE')
    )
    TASK_STATUS = (
        ('NOT_STARTED', 'NOT_STARTED'),
        ('IN_PROGRESS', 'IN_PROGRESS'),
        ('COMPLETED', 'COMPLETED'),
        ('FLAGGED', 'FLAGGED')
    )
    application_id = models.UUIDField(primary_key=True, default=uuid4)
    application_type = models.CharField(choices=APP_TYPE, max_length=50, blank=True)
    application_status = models.CharField(choices=APP_STATUS, max_length=50, blank=True)
    cygnum_urn = models.CharField(max_length=50, blank=True)
    login_details_status = models.CharField(choices=TASK_STATUS, max_length=50)
    login_details_arc_flagged = models.BooleanField(default=False)
    personal_details_status = models.CharField(choices=TASK_STATUS, max_length=50)
    personal_details_arc_flagged = models.BooleanField(default=False)
    childcare_type_status = models.CharField(choices=TASK_STATUS, max_length=50)
    childcare_type_arc_flagged = models.BooleanField(default=False)
    first_aid_training_status = models.CharField(choices=TASK_STATUS, max_length=50)
    first_aid_training_arc_flagged = models.BooleanField(default=False)
    eyfs_training_status = models.CharField(choices=TASK_STATUS, max_length=50)
    eyfs_training_arc_flagged = models.BooleanField(default=False)
    criminal_record_check_status = models.CharField(choices=TASK_STATUS, max_length=50)
    criminal_record_check_arc_flagged = models.BooleanField(default=False)
    health_status = models.CharField(choices=TASK_STATUS, max_length=50)
    health_arc_flagged = models.BooleanField(default=False)
    references_status = models.CharField(choices=TASK_STATUS, max_length=50)
    references_arc_flagged = models.BooleanField(default=False)
    people_in_home_status = models.CharField(choices=TASK_STATUS, max_length=50)
    people_in_home_arc_flagged = models.BooleanField(default=False)
    adults_in_home = models.NullBooleanField(blank=True, null=True, default=None)
    children_in_home = models.NullBooleanField(blank=True, null=True, default=None)
    children_turning_16 = models.NullBooleanField(blank=True, null=True, default=None)
    declarations_status = models.CharField(choices=TASK_STATUS, max_length=50)
    share_info_declare = models.NullBooleanField(blank=True, null=True, default=None)
    display_contact_details_on_web = models.NullBooleanField(blank=True, null=True, default=None)
    information_correct_declare = models.NullBooleanField(blank=True, null=True, default=None)
    change_declare = models.NullBooleanField(blank=True, null=True, default=None)
    date_created = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    date_accepted = models.DateTimeField(blank=True, null=True)
    order_code = models.UUIDField(blank=True, null=True)
    date_submitted = models.DateTimeField(blank=True, null=True)

    @classmethod
    def get_id(cls, app_id):
        return cls.objects.get(pk=app_id)

    class Meta:
        db_table = 'APPLICATION'


class UserDetails(models.Model):
    """
    Model for USER_DETAILS table
    """
    login_id = models.UUIDField(primary_key=True, default=uuid4)
    application_id = models.ForeignKey(Application, on_delete=models.CASCADE, db_column='application_id', default=uuid4)
    email = models.CharField(max_length=100, blank=True)
    mobile_number = models.CharField(max_length=20, blank=True)
    add_phone_number = models.CharField(max_length=20, blank=True)
    email_expiry_date = models.IntegerField(blank=True, null=True)
    sms_expiry_date = models.IntegerField(blank=True, null=True)
    magic_link_email = models.CharField(max_length=100, blank=True, null=True)
    magic_link_sms = models.CharField(max_length=100, blank=True, null=True)
    security_question = models.CharField(max_length=100, blank=True, null=True)
    security_answer = models.CharField(max_length=100, blank=True, null=True)

    @property
    def timelog_fields(self):
        """
        Specify which fields to track in this model once application is returned.
        Used for signals only. Check base.py for available signals.
        This is used for logging fields which gonna be updated by applicant
        once application status changed to "FURTHER_INFORMATION" on the arc side
        Returns:
            tuple of fields which needs update tracking when application is returned
        """

        return (
            'email',
            'mobile_number',
            'add_phone_number',
            'security_question',
            'security_answer'
        )

    class Meta:
        db_table = 'USER_DETAILS'


class ChildcareType(models.Model):
    """
    Model for CHILDCARE_TYPE table
    """
    childcare_id = models.UUIDField(primary_key=True, default=uuid4)
    application_id = models.ForeignKey(Application, on_delete=models.CASCADE, db_column='application_id')
    zero_to_five = models.BooleanField()
    five_to_eight = models.BooleanField()
    eight_plus = models.BooleanField()
    overnight_care = models.NullBooleanField()

    @property
    def timelog_fields(self):
        """
        Specify which fields to track in this model once application is returned.
        Used for signals only. Check base.py for available signals.
        This is used for logging fields which gonna be updated by applicant
        once application status changed to "FURTHER_INFORMATION" on the arc side
        Returns:
            tuple of fields which needs update tracking when application is returned
        """

        return (
            'zero_to_five',
            'five_to_eight',
            'eight_plus',
            'overnight_care'
        )

    @classmethod
    def get_id(cls, app_id):
        return cls.objects.get(application_id=app_id)

    class Meta:
        db_table = 'CHILDCARE_TYPE'


class ApplicantPersonalDetails(models.Model):
    """
    Model for APPLICANT_PERSONAL_DETAILS table
    """
    personal_detail_id = models.UUIDField(primary_key=True, default=uuid4)
    application_id = models.ForeignKey(Application, on_delete=models.CASCADE, db_column='application_id')
    birth_day = models.IntegerField(blank=True, null=True)
    birth_month = models.IntegerField(blank=True, null=True)
    birth_year = models.IntegerField(blank=True, null=True)

    @property
    def timelog_fields(self):
        """
        Specify which fields to track in this model once application is returned.
        Used for signals only. Check base.py for available signals.
        This is used for logging fields which gonna be updated by applicant
        once application status changed to "FURTHER_INFORMATION" on the arc side
        Returns:
            tuple of fields which needs update tracking when application is returned
        """

        return ('birth_day', 'birth_month', 'birth_year',)

    @classmethod
    def get_id(cls, app_id):
        return cls.objects.get(application_id=app_id)

    class Meta:
        db_table = 'APPLICANT_PERSONAL_DETAILS'


class ApplicantName(models.Model):
    """
    Model for APPLICANT_NAME table
    """
    name_id = models.UUIDField(primary_key=True, default=uuid4)
    personal_detail_id = models.ForeignKey(ApplicantPersonalDetails, on_delete=models.CASCADE,
                                           db_column='personal_detail_id')
    application_id = models.ForeignKey(Application, on_delete=models.CASCADE,
                                       db_column='application_id')
    current_name = models.BooleanField(blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    middle_names = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    # TODO Might not work - need to test
    @classmethod
    def get_id(cls, app_id):
        personal_detail_id = ApplicantPersonalDetails.get_id(app_id)
        return cls.objects.get(personal_detail_id=personal_detail_id)

    @property
    def timelog_fields(self):
        """
        Specify which fields to track in this model once application is returned.
        Used for signals only. Check base.py for available signals.
        This is used for logging fields which gonna be updated by applicant
        once application status changed to "FURTHER_INFORMATION" on the arc side
        Returns:
            tuple of fields which needs update tracking when application is returned
        """

        return ('first_name', 'last_name', 'middle_names',)

    class Meta:
        db_table = 'APPLICANT_NAME'


class ApplicantHomeAddress(models.Model):
    """
    Model for APPLICANT_HOME_ADDRESS table
    """
    home_address_id = models.UUIDField(primary_key=True, default=uuid4)
    personal_detail_id = models.ForeignKey(ApplicantPersonalDetails, on_delete=models.CASCADE,
                                           db_column='personal_detail_id')
    application_id = models.ForeignKey(Application, on_delete=models.CASCADE,
                                       db_column='application_id')
    street_line1 = models.CharField(max_length=100, blank=True)
    street_line2 = models.CharField(max_length=100, blank=True)
    town = models.CharField(max_length=100, blank=True)
    county = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=8, blank=True)
    childcare_address = models.NullBooleanField(blank=True, null=True, default=None)
    current_address = models.NullBooleanField(blank=True, null=True, default=None)
    move_in_month = models.IntegerField(blank=True)
    move_in_year = models.IntegerField(blank=True)

    @property
    def timelog_fields(self):
        """
        Specify which fields to track in this model once application is returned.
        Used for signals only. Check base.py for available signals.
        This is used for logging fields which gonna be updated by applicant
        once application status changed to "FURTHER_INFORMATION" on the arc side
        Returns:
            tuple of fields which needs update tracking when application is returned
        """

        return (
            'street_line1',
            'street_line2',
            'town',
            'county',
            'country',
            'postcode',
            'childcare_address',
            'current_address',
            'move_in_month',
            'move_in_year'
        )


    @classmethod
    def get_id(cls, app_id):
        personal_detail_id = ApplicantPersonalDetails.get_id(app_id)
        return cls.objects.get(personal_detail_id=personal_detail_id)

    class Meta:
        db_table = 'APPLICANT_HOME_ADDRESS'


class FirstAidTraining(models.Model):
    """
    Model for FIRST_AID_TRAINING table
    """
    first_aid_id = models.UUIDField(primary_key=True, default=uuid4)
    application_id = models.ForeignKey(
        Application, on_delete=models.CASCADE, db_column='application_id')
    training_organisation = models.CharField(max_length=100)
    course_title = models.CharField(max_length=100)
    course_day = models.IntegerField()
    course_month = models.IntegerField()
    course_year = models.IntegerField()
    show_certificate = models.NullBooleanField(blank=True, null=True, default=None)
    renew_certificate = models.NullBooleanField(blank=True, null=True, default=None)

    @property
    def timelog_fields(self):
        """
        Specify which fields to track in this model once application is returned.
        Used for signals only. Check base.py for available signals.
        This is used for logging fields which gonna be updated by applicant
        once application status changed to "FURTHER_INFORMATION" on the arc side
        Returns:
            tuple of fields which needs update tracking when application is returned
        """

        return (
            'training_organisation',
            'course_title',
            'course_day',
            'course_month',
            'course_year',
            'show_certificate',
            'renew_certificate'
        )

    @classmethod
    def get_id(cls, app_id):
        return cls.objects.get(application_id=app_id)

    class Meta:
        db_table = 'FIRST_AID_TRAINING'


class EYFS(models.Model):
    """
    Model for EYFS table
    """
    eyfs_id = models.UUIDField(primary_key=True, default=uuid4)
    application_id = models.ForeignKey(
        Application, on_delete=models.CASCADE, db_column='application_id')
    eyfs_course_name = models.CharField(max_length=50, blank=True, )
    eyfs_course_date_day = models.IntegerField(blank=True, null=True)
    eyfs_course_date_month = models.IntegerField(blank=True, null=True)
    eyfs_course_date_year = models.IntegerField(blank=True, null=True)

    @property
    def timelog_fields(self):
        """
        Specify which fields to track in this model once application is returned.
        Used for signals only. Check base.py for available signals.
        This is used for logging fields which gonna be updated by applicant
        once application status changed to "FURTHER_INFORMATION" on the arc side
        Returns:
            tuple of fields which needs update tracking when application is returned
        """

        return (
            'eyfs_course_name',
            'eyfs_course_date_day',
            'eyfs_course_date_month',
            'eyfs_course_date_year'
        )

    @classmethod
    def get_id(cls, app_id):
        return cls.objects.get(application_id=app_id)

    class Meta:
        db_table = 'EYFS'


class CriminalRecordCheck(models.Model):
    """
    Model for CRIMINAL_RECORD_CHECK table
    """
    criminal_record_id = models.UUIDField(primary_key=True, default=uuid4)
    application_id = models.ForeignKey(
        Application, on_delete=models.CASCADE, db_column='application_id')
    dbs_certificate_number = models.CharField(max_length=50, blank=True)
    cautions_convictions = models.BooleanField(blank=True)

    @property
    def timelog_fields(self):
        """
        Specify which fields to track in this model once application is returned.
        Used for signals only. Check base.py for available signals.
        This is used for logging fields which gonna be updated by applicant
        once application status changed to "FURTHER_INFORMATION" on the arc side
        Returns:
            tuple of fields which needs update tracking when application is returned
        """

        return (
            'dbs_certificate_number',
            'cautions_convictions'
        )

    @classmethod
    def get_id(cls, app_id):
        return cls.objects.get(application_id=app_id)

    class Meta:
        db_table = 'CRIMINAL_RECORD_CHECK'


class HealthDeclarationBooklet(models.Model):
    """
    Model for HEALTH_DECLARATION_BOOKLET table
    """
    hdb_id = models.UUIDField(primary_key=True, default=uuid4)
    application_id = models.ForeignKey(
        Application, on_delete=models.CASCADE, db_column='application_id')
    send_hdb_declare = models.NullBooleanField(blank=True)

    @property
    def timelog_fields(self):
        """
        Specify which fields to track in this model once application is returned.
        Used for signals only. Check base.py for available signals.
        This is used for logging fields which gonna be updated by applicant
        once application status changed to "FURTHER_INFORMATION" on the arc side
        Returns:
            tuple of fields which needs update tracking when application is returned
        """

        return (
            'send_hdb_declare',
        )

    @classmethod
    def get_id(cls, app_id):
        return cls.objects.get(application_id=app_id)

    class Meta:
        db_table = 'HDB'


class Reference(models.Model):
    """
    Model for REFERENCE table
    """
    reference_id = models.UUIDField(primary_key=True, default=uuid4)
    application_id = models.ForeignKey(Application, on_delete=models.CASCADE, db_column='application_id')
    reference = models.IntegerField(blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    relationship = models.CharField(max_length=100, blank=True)
    years_known = models.IntegerField(blank=True)
    months_known = models.IntegerField(blank=True)
    street_line1 = models.CharField(max_length=100, blank=True)
    street_line2 = models.CharField(max_length=100, blank=True)
    town = models.CharField(max_length=100, blank=True)
    county = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=8, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=100, blank=True)

    @property
    def timelog_fields(self):
        """
        Specify which fields to track in this model once application is returned.
        Used for signals only. Check base.py for available signals.
        This is used for logging fields which gonna be updated by applicant
        once application status changed to "FURTHER_INFORMATION" on the arc side
        Returns:
            tuple of fields which needs update tracking when application is returned
        """

        return (
            'reference',
            'first_name',
            'last_name',
            'relationship',
            'years_known',
            'months_known',
            'street_line1',
            'street_line2',
            'town',
            'county',
            'country',
            'postcode',
            'phone_number',
            'email'
        )

    @classmethod
    def get_id(cls, app_id):
        return cls.objects.get(application_id=app_id)

    class Meta:
        db_table = 'REFERENCE'


class AdultInHome(models.Model):
    """
    Model for ADULT_IN_HOME table
    """
    adult_id = models.UUIDField(primary_key=True, default=uuid4)
    application_id = models.ForeignKey(
        Application, on_delete=models.CASCADE, db_column='application_id')
    adult = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    middle_names = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    birth_day = models.IntegerField(blank=True)
    birth_month = models.IntegerField(blank=True)
    birth_year = models.IntegerField(blank=True)
    relationship = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    dbs_certificate_number = models.CharField(max_length=50, blank=True)
    token = models.CharField(max_length=100, blank=True, null=True)
    validated = models.BooleanField(default=False)
    current_treatment = models.BooleanField(default=False)
    serious_illness = models.BooleanField(default=False)
    hospital_admission = models.BooleanField(default=False)
    health_check_status = models.CharField(max_length=50, default='To do')
    email_resent = models.IntegerField(default=0)
    email_resent_timestamp = models.DateTimeField(null=True, blank=True)

    @property
    def timelog_fields(self):
        """
        Specify which fields to track in this model once application is returned.
        Used for signals only. Check base.py for available signals.
        This is used for logging fields which gonna be updated by applicant
        once application status changed to "FURTHER_INFORMATION" on the arc side
        Returns:
            tuple of fields which needs update tracking when application is returned
        """

        return (
            'adult',
            'first_name',
            'middle_names',
            'last_name',
            'birth_day',
            'birth_month',
            'birth_year',
            'relationship',
            'email',
            'dbs_certificate_number',
            'health_check_status'
        )

    @classmethod
    def get_id(cls, app_id):
        return cls.objects.get(application_id=app_id)

    @property
    def date_of_birth(self):
        return datetime(year=self.birth_year, month=self.birth_month, day=self.birth_day)

    class Meta:
        db_table = 'ADULT_IN_HOME'


class ChildInHome(models.Model):
    """
    Model for CHILD_IN_HOME table
    """
    child_id = models.UUIDField(primary_key=True, default=uuid4)
    application_id = models.ForeignKey(
        Application, on_delete=models.CASCADE, db_column='application_id')
    child = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    middle_names = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    birth_day = models.IntegerField(blank=True)
    birth_month = models.IntegerField(blank=True)
    birth_year = models.IntegerField(blank=True)
    relationship = models.CharField(max_length=100, blank=True)

    @classmethod
    def get_id(cls, app_id):
        return cls.objects.get(application_id=app_id)

    @property
    def timelog_fields(self):
        """
        Specify which fields to track in this model once application is returned.
        Used for signals only. Check base.py for available signals.
        This is used for logging fields which gonna be updated by applicant
        once application status changed to "FURTHER_INFORMATION" on the arc side
        Returns:
            tuple of fields which needs update tracking when application is returned
        """

        return (
            'child',
            'first_name',
            'middle_names',
            'last_name',
            'birth_day',
            'birth_month',
            'birth_year',
            'relationship'
        )

    class Meta:
        db_table = 'CHILD_IN_HOME'
