'''
Created on Jun 22, 2018

@author: moffat
'''
from django.test import TestCase, tag
from django.core.exceptions import ValidationError
from django.utils import timezone
from ..forms import IneligibleSubjectFormValidator


@tag('T')
class TestInEligibleFormValidator(TestCase):

    def setUp(self):
        self.options = {
            'report_datetime': timezone.now(),
            'screening_identifier': 'S9912312',
            'reasons_ineligible': 'Blah blah blah'}

    def test_vailation_raised_with_no_reasons(self):
        self.options['reasons_ineligible'] = None
        form_validator = IneligibleSubjectFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('reasons_ineligible', form_validator._errors)

    def test_vailation_raised_with_no_identifier(self):
        self.options['screening_identifier'] = None
        form_validator = IneligibleSubjectFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('screening_identifier', form_validator._errors)