'''
Created on Jun 22, 2018

@author: moffat
'''
from django.test import TestCase, tag
from django.core.exceptions import ValidationError
from edc_constants.constants import YES, NO, NOT_APPLICABLE, MALE, FEMALE
from django.utils import timezone
from ..form_validator import SubjectScreeningFormValidator
from copy import copy
from edc_form_validators.base_form_validator import ModelFormFieldValidatorError, InvalidModelFormFieldValidator


@tag('form_validator')
class TestSubjectScreeningFormValidator(TestCase):

    def setUp(self):
        self.subject_details = {
            'report_datetime': timezone.now(),
            'age_in_years': 20,
            'gender': MALE,
            'citizen': YES,
            'married_to_citizen': NOT_APPLICABLE,
            'marriage_proof': NOT_APPLICABLE,
            'is_literate': YES,
            'literate_witness_present': NOT_APPLICABLE,
            'guardian_present': NOT_APPLICABLE
            }
        pass

    def test_subject_form_validator_cleaned_data_is_none(self):
        """Asserts raises if cleaned data is None; that is, not
        provided.
        """
        self.assertRaises(ModelFormFieldValidatorError,
                          SubjectScreeningFormValidator, cleaned_data=None)

    def test_subject_form_validator_no_response(self):
        """Asserts raises if no response provided.
        """
        form_validator = SubjectScreeningFormValidator(cleaned_data={})
        self.assertRaises(
            InvalidModelFormFieldValidator,
            form_validator.required_if)

        def test_no_field(self):
            """Asserts raises if no field provided.
            """
            form_validator = SubjectScreeningFormValidator(cleaned_data={})
            self.assertRaises(
                InvalidModelFormFieldValidator,
                form_validator.required_if, YES)

    def test_guardian_field_required_ok(self):
        current_details = copy(self.subject_details)
        current_details['age_in_years'] = 10
        current_details['guardian_present'] = NOT_APPLICABLE
        condition = current_details['age_in_years'] < 18
        validator = SubjectScreeningFormValidator(cleaned_data=current_details)
        self.assertRaises(
            ValidationError,
            validator.required_if_true,
            condition=condition, field='age_in_years',
                                       field_required='guardian_present')

    def test_married_to_citizen_field_applicable_ok(self):
        current_details = copy(self.subject_details)
        current_details['citizen'] = NO
        current_details['married_to_citizen'] = YES
        validator = SubjectScreeningFormValidator(cleaned_data=current_details)
        self.assertRaises(
            ValidationError,
            validator.applicable_if,
            YES, field='citizen',
            field_applicable='married_to_citizen')

    def test_married_to_citizen_field_not_applicable_ok(self):
        current_details = copy(self.subject_details)
        current_details['married_to_citizen'] = NO
        validator = SubjectScreeningFormValidator(cleaned_data=current_details)
        self.assertRaises(
            ValidationError,
            validator.not_applicable_if,
            YES, field='citizen',
            field_applicable='married_to_citizen')

    def test_literate_witness_not_applicable_ok(self):
        current_details = copy(self.subject_details)
        current_details['literate'] = YES
        current_details['literate_witness_present'] = NO
        validator = SubjectScreeningFormValidator(cleaned_data=current_details)
        self.assertRaises(
            ValidationError,
            validator.not_applicable_if,
            YES, field='literate',
            field_applicable='literate_witness_present')
        pass

    def test_literate_witness_applicable_ok(self):
        current_details = copy(self.subject_details)
        current_details['literate'] = NO
        current_details['literate_witness_present'] = NOT_APPLICABLE
        validator = SubjectScreeningFormValidator(cleaned_data=current_details)
        self.assertRaises(
            ValidationError,
            validator.applicable_if,
            NO, field='literate',
            field_applicable='literate_witness_present')

    def test_marriage_proof_not_applicable_ok(self):
        current_details = copy(self.subject_details)
        current_details['married_to_citizen'] = NO
        validator = SubjectScreeningFormValidator(cleaned_data=current_details)
        self.assertRaises(
            ValidationError,
            validator.not_applicable_if,
            YES, field='married_to_citizen',
            field_applicable='marriage_proof')

    def test_marriage_proof_applicable_ok(self):
        current_details = copy(self.subject_details)
        current_details['married_to_citizen'] = YES
        validator = SubjectScreeningFormValidator(cleaned_data=current_details)
        self.assertRaises(
            ValidationError,
            validator.applicable_if,
            YES, field='married_to_citizen',
            field_applicable='marriage_proof')

    def test_not_married_to_citizen_no_certificate(self):
        self.subject_details['citizen'] = NO
        self.subject_details['married_to_citizen'] = NOT_APPLICABLE
        form_validator = SubjectScreeningFormValidator(
            cleaned_data=self.subject_details)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_not_literate_no_witness(self):
        self.subject_details['literate'] = NO
        self.subject_details['literate_witness_present'] = NOT_APPLICABLE
        form_validator = SubjectScreeningFormValidator(
            cleaned_data=self.subject_details)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_minor_no_guardian(self):
        self.subject_details['age_in_years'] = 18
        self.subject_details['guardian_present'] = YES
        form_validator = SubjectScreeningFormValidator(
            cleaned_data=self.subject_details)
        self.assertRaises(ValidationError, form_validator.validate)



