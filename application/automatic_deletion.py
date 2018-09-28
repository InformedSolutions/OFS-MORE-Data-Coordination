import logging

from .models import (AdultInHome,
                     ApplicantHomeAddress,
                     ApplicantName,
                     ApplicantPersonalDetails,
                     Application,
                     Arc,
                     Child,
                     ChildAddress,
                     ChildInHome,
                     ChildcareTraining,
                     ChildcareType,
                     CriminalRecordCheck,
                     FirstAidTraining,
                     HealthDeclarationBooklet,
                     HealthCheckCurrent,
                     HealthCheckHospital,
                     HealthCheckSerious,
                     OtherPersonPreviousRegistrationDetails,
                     Payment,
                     PreviousAddress,
                     PreviousName,
                     PreviousRegistrationDetails,
                     Reference,
                     UserDetails)
from django.conf import settings
from datetime import datetime, timedelta

from django_cron import CronJobBase, Schedule


class automatic_deletion(CronJobBase):
    RUN_EVERY_MINS = settings.AUTOMATIC_DELETION_FREQUENCY

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'application.automatic_deletion'

    def do(self):
        log = logging.getLogger('django.server')
        log.info('Checking for expired applications')
        ninety_days_ago = datetime.now() - timedelta(days=90)
        # Determine expired applications based on date last accessed
        expired_submissions = list(
            Application.objects.filter(application_status='DRAFTING', date_last_accessed__lte=ninety_days_ago))

        for submission in expired_submissions:
            log.info(str(datetime.now()) + ' - Deleting application: ' + str(submission.pk))
            # Delete associated records
            if AdultInHome.objects.filter(application_id=submission.pk).exists():
                adult_in_home_records = list(AdultInHome.objects.filter(application_id=submission.pk))
                for adult_in_home_record in adult_in_home_records:
                    log.info(str(datetime.now()) + ' - Deleting adult in home record: ' + str(adult_in_home_record.pk))
                    adult_in_home_record.delete()

                    if HealthCheckCurrent.objects.filter(person_id=adult_in_home_record.pk).exists():
                        current_health_records = list(
                            HealthCheckCurrent.objects.filter(person_id=adult_in_home_record.pk))
                        for current_health_record in current_health_records:
                            log.info(
                                str(datetime.now()) + ' - Deleting current health record: ' + str(
                                    current_health_record.pk))
                            current_health_record.delete()

                    if HealthCheckHospital.objects.filter(person_id=adult_in_home_record.pk).exists():
                        hospital_health_records = list(
                            HealthCheckHospital.objects.filter(person_id=adult_in_home_record.pk))
                        for hospital_health_record in hospital_health_records:
                            log.info(
                                str(datetime.now()) + ' - Deleting hospital health record: ' + str(
                                    hospital_health_record.pk))
                            hospital_health_record.delete()

                    if HealthCheckSerious.objects.filter(person_id=adult_in_home_record.pk).exists():
                        serious_health_records = list(
                            HealthCheckSerious.objects.filter(person_id=adult_in_home_record.pk))
                        for serious_health_record in serious_health_records:
                            log.info(
                                str(datetime.now()) + ' - Deleting serious health record: ' + str(
                                    serious_health_record.pk))
                            serious_health_record.delete()

                    if OtherPersonPreviousRegistrationDetails.objects.filter(
                            person_id=adult_in_home_record.pk).exists():
                        other_person_previous_registration_records = list(
                            OtherPersonPreviousRegistrationDetails.objects.filter(person_id=adult_in_home_record.pk))
                        for other_person_previous_registration_record in other_person_previous_registration_records:
                            log.info(
                                str(datetime.now()) + ' - Deleting other person previous registration record: ' + str(
                                    other_person_previous_registration_record.pk))
                            other_person_previous_registration_record.delete()

                    if PreviousAddress.objects.filter(person_id=adult_in_home_record.pk).exists():
                        previous_address_records = list(
                            PreviousAddress.objects.filter(person_id=adult_in_home_record.pk))
                        for previous_address_record in previous_address_records:
                            log.info(
                                str(datetime.now()) + ' - Deleting previous address record: ' + str(
                                    previous_address_record.pk))
                            previous_address_record.delete()

                    if PreviousName.objects.filter(person_id=adult_in_home_record.pk).exists():
                        previous_name_records = list(PreviousName.objects.filter(person_id=adult_in_home_record.pk))
                        for previous_name_record in previous_name_records:
                            log.info(str(datetime.now()) + ' - Deleting previous name record: ' + str(
                                previous_name_record.pk))
                            previous_name_record.delete()

            if ApplicantHomeAddress.objects.filter(application_id=submission.pk).exists():
                applicant_address_records = list(ApplicantHomeAddress.objects.filter(application_id=submission.pk))
                for applicant_address_record in applicant_address_records:
                    log.info(str(datetime.now()) + ' - Deleting applicant address record: ' + str(
                        applicant_address_record.pk))
                    applicant_address_record.delete()

            if ApplicantName.objects.filter(application_id=submission.pk).exists():
                applicant_name_records = list(ApplicantName.objects.filter(application_id=submission.pk))
                for applicant_name_record in applicant_name_records:
                    log.info(str(datetime.now()) + ' - Deleting applicant name record: ' + str(
                        applicant_name_record.pk))
                    applicant_name_record.delete()

            if ApplicantPersonalDetails.objects.filter(application_id=submission.pk).exists():
                applicant_personal_details_records = list(
                    ApplicantPersonalDetails.objects.filter(application_id=submission.pk))
                for applicant_personal_details_record in applicant_personal_details_records:
                    log.info(str(datetime.now()) + ' - Deleting applicant personal details record: ' + str(
                        applicant_personal_details_record.pk))
                    applicant_personal_details_record.delete()

            if Arc.objects.filter(application_id=submission.pk).exists():
                arc_records = list(Arc.objects.filter(application_id=submission.pk))
                for arc_record in arc_records:
                    log.info(str(datetime.now()) + ' - Deleting ARC record: ' + str(arc_record.pk))
                    arc_record.delete()

            if Child.objects.filter(application_id=submission.pk).exists():
                child_records = list(Child.objects.filter(application_id=submission.pk))
                for child_record in child_records:
                    log.info(str(datetime.now()) + ' - Deleting child record: ' + str(child_record.pk))
                    child_record.delete()

            if ChildAddress.objects.filter(application_id=submission.pk).exists():
                child_address_records = list(ChildAddress.objects.filter(application_id=submission.pk))
                for child_address_record in child_address_records:
                    log.info(str(datetime.now()) + ' - Deleting child address record: ' + str(child_address_record.pk))
                    child_address_record.delete()

            if ChildInHome.objects.filter(application_id=submission.pk).exists():
                child_in_home_records = list(ChildInHome.objects.filter(application_id=submission.pk))
                for child_in_home_record in child_in_home_records:
                    log.info(str(datetime.now()) + ' - Deleting child in home record: ' + str(child_in_home_record.pk))
                    child_in_home_record.delete()

                    if PreviousAddress.objects.filter(person_id=child_in_home_record.pk).exists():
                        previous_address_records = list(
                            PreviousAddress.objects.filter(person_id=child_in_home_record.pk))
                        for previous_address_record in previous_address_records:
                            log.info(
                                str(datetime.now()) + ' - Deleting previous address record: ' + str(
                                    previous_address_record.pk))
                            previous_address_record.delete()

                    if PreviousName.objects.filter(person_id=child_in_home_record.pk).exists():
                        previous_name_records = list(PreviousName.objects.filter(person_id=child_in_home_record.pk))
                        for previous_name_record in previous_name_records:
                            log.info(str(datetime.now()) + ' - Deleting previous name record: ' + str(
                                previous_name_record.pk))
                            previous_name_record.delete()

            if ChildcareTraining.objects.filter(application_id=submission.pk).exists():
                childcare_training_records = list(ChildcareTraining.objects.filter(application_id=submission.pk))
                for childcare_training_record in childcare_training_records:
                    log.info(str(datetime.now()) + ' - Deleting childcare training record: ' + str(
                        childcare_training_record.pk))
                    childcare_training_record.delete()

            if ChildcareType.objects.filter(application_id=submission.pk).exists():
                childcare_type_records = list(ChildcareType.objects.filter(application_id=submission.pk))
                for childcare_type_record in childcare_type_records:
                    log.info(
                        str(datetime.now()) + ' - Deleting childcare type record: ' + str(childcare_type_record.pk))
                    childcare_type_record.delete()

            if CriminalRecordCheck.objects.filter(application_id=submission.pk).exists():
                criminal_record_check_records = list(CriminalRecordCheck.objects.filter(application_id=submission.pk))
                for criminal_record_check_record in criminal_record_check_records:
                    log.info(str(datetime.now()) + ' - Deleting criminal record check record: ' + str(
                        criminal_record_check_record.pk))
                    criminal_record_check_record.delete()

            if FirstAidTraining.objects.filter(application_id=submission.pk).exists():
                first_aid_training_records = list(FirstAidTraining.objects.filter(application_id=submission.pk))
                for first_aid_training_record in first_aid_training_records:
                    log.info(str(datetime.now()) + ' - Deleting first aid training record: ' + str(
                        first_aid_training_record.pk))
                    first_aid_training_record.delete()

            if HealthDeclarationBooklet.objects.filter(application_id=submission.pk).exists():
                health_records = list(HealthDeclarationBooklet.objects.filter(application_id=submission.pk))
                for health_record in health_records:
                    log.info(str(datetime.now()) + ' - Deleting health record: ' + str(health_record.pk))
                    health_record.delete()

            if Payment.objects.filter(application_id=submission.pk).exists():
                payment_records = list(Payment.objects.filter(application_id=submission.pk))
                for payment_record in payment_records:
                    log.info(str(datetime.now()) + ' - Deleting payment record: ' + str(payment_record.pk))
                    payment_record.delete()

            if PreviousRegistrationDetails.objects.filter(application_id=submission.pk).exists():
                previous_registration_details_records = list(
                    PreviousRegistrationDetails.objects.filter(application_id=submission.pk))
                for previous_registration_details_record in previous_registration_details_records:
                    log.info(str(datetime.now()) + ' - Deleting previous registration details record: ' + str(
                        previous_registration_details_record.pk))
                    previous_registration_details_record.delete()

            if Reference.objects.filter(application_id=submission.pk).exists():
                reference_records = list(Reference.objects.filter(application_id=submission.pk))
                for reference_record in reference_records:
                    log.info(str(datetime.now()) + ' - Deleting reference record: ' + str(reference_record.pk))
                    reference_record.delete()

            if UserDetails.objects.filter(application_id=submission.pk).exists():
                user_details_records = list(UserDetails.objects.filter(application_id=submission.pk))
                for user_details_record in user_details_records:
                    log.info(str(datetime.now()) + ' - Deleting user details record: ' + str(user_details_record.pk))
                    user_details_record.delete()

            # Delete Application
            submission.delete()
