'''
Created on Jun 18, 2018

@author: moffat
'''
from edc_base.utils import get_utcnow
from ..eligibility import Eligibility, EligibilityError
from django.test import TestCase, tag
from copy import copy


@tag('eligibility')
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
            marriage_certificate_present=True,
            literate=True,
            literate_witness_present=True)

        self.criteria = dict()

    def test_eligibility_with_criteria(self):
        eligibility = Eligibility(**self.evaluator_criteria)
        self.assertTrue(eligibility.eligible)
        self.assertEqual(eligibility.reasons_ineligible, {'none': 'None'})

    @tag('test_eligible')
    def test_eligible(self):
        criteria = copy(self.evaluator_criteria)
        criteria.update({'marriage_certificate_present': False})
        criteria.update({'literate_witness_present': False})
        obj = Eligibility(**criteria)
        self.assertTrue(obj.eligible)

    def test_eligibility_not_ok_by_age(self):
        self.evaluator_criteria.update(age_in_years=17)
        self.evaluator_criteria.update(guardian_present=False)
        eligibility = Eligibility(**self.evaluator_criteria)
        self.assertFalse(eligibility.eligible)

    @tag('test_not_eligible')
    def test_not_eligible(self):
        criteria = copy(self.evaluator_criteria)
        criteria.update({'literate': False})
        criteria.update({'literate_witness_present': False})
        obj = Eligibility(**criteria)
        self.assertFalse(obj.eligible)
        self.assertIn('literate', obj.reasons_ineligible)