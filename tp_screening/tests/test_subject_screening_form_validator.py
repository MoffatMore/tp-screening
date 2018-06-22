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


