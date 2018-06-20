'''
Created on Jun 18, 2018

@author: moffat
'''
from edc_base.utils import get_utcnow
from ..eligibility import Eligibility, EligibilityError
from django.test import TestCase, tag


class TestEligibility(TestCase):
    '''
    classdocs
    '''

    def setUp(self):
        self.evaluator_criteria = dict(
            age_in_years=20,
            guardian_present=True,
            citizen=True,
            married_to_citizen=True,
            documents_present=True,
            literate=True,
            witness_available=True)

        self.criteria = dict()

    @tag('without_criteria')
    def test_eligibility_without_criteria(self):
        self.assertRaises(TypeError,Eligibility)
