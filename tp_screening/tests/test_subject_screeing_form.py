'''
Created on Jun 22, 2018

@author: moffat
'''

from django.test import TestCase, tag
from edc_constants.constants import YES, FEMALE, NO, NOT_APPLICABLE
from ..forms import SubjectScreeningForm
from edc_base.utils import get_utcnow
from copy import copy


@tag('TestSubjectForm')
class TestSubjectScreeningForm(TestCase):

    def setUp(self):
        self.screening_data = dict(
            subject_identifier='12345',
            report_datetime=get_utcnow(),
            gender=FEMALE,
            age_in_years=23,
            guardian_present=NOT_APPLICABLE,
            citizen=YES,
            married_to_citizen=NOT_APPLICABLE,
            marriage_certificate_present=NOT_APPLICABLE,
            literate=YES,
            literate_witness_present=NOT_APPLICABLE,
            consent_ability=YES,
            consented=YES,
            reasons_ineligible={'None'})

    def test_default_ok(self):
        form = SubjectScreeningForm(data=self.screening_data)
        form.is_valid()
        self.assertEqual(form.errors, {})
        self.assertTrue(form.save())

    def test_citizen_married_to_citizen_not_applicable(self):
        """test when a participant is a citizen and
           is_married_citizen is not applicable"""
        data = copy(self.screening_data)
        data.update(
            citizen=YES,
            married_to_citizen=YES,
            marriage_certificate_present=YES)
        form = SubjectScreeningForm(data=data)
        form.is_valid()
        self.assertEqual(
            form.errors, {'married_to_citizen':
                          ['This field is not applicable']})

    def test_not_literate_witness_not_applicable(self):
        data = copy(self.screening_data)
        data.update(
            literate=NO)
        form = SubjectScreeningForm(data=data)
        form.is_valid()
        self.assertEqual(
            form.errors, {'literate_witness_present':
                          ['This field is applicable']})

    def test_is_minor_guardian_none(self):
        data = copy(self.screening_data)
        data.update(
            age_in_years=8)
        form = SubjectScreeningForm(data=data)
        form.is_valid()
        self.assertEqual(
            form.errors, {'guardian_present':
                          ['This field is required.']})
