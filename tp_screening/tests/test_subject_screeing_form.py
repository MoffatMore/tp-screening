'''
Created on Jun 22, 2018

@author: moffat
'''

from django.test import TestCase, tag
from ..forms import SubjectScreeningForm
from edc_constants.constants import YES, FEMALE, NO, NOT_APPLICABLE, MALE
from edc_base.utils import get_utcnow
from copy import copy


class TestSubjectScreeningForm(TestCase):
    """Subject Screening form test"""

    @tag('form_ok')
    def test_subject_screen_form_ok(self):
        form = dict(
            screening_identifier='11111',
            report_datetime=get_utcnow(),
            gender=MALE,
            age_in_years=18,
            guardian_present=NOT_APPLICABLE,
            citizen=YES,
            married_to_citizen=NOT_APPLICABLE,
            marriage_certificate_present=NOT_APPLICABLE,
            literate=YES,
            literate_witness_present=NOT_APPLICABLE,
            consent_ability=YES,
            consented=YES,
            reasons_ineligible={'None'})
        subject_form = SubjectScreeningForm(data=form)
#         self.assertTrue(subject_form.is_valid())

