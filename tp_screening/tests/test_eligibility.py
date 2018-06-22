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
            married_to_citizen=False,
            marriage_certificate_present=False,
            literate=True,
            literate_witness_present=False)

        self.criteria = dict()

    def test_eligibility_with_criteria(self):
        eligibility = Eligibility(**self.evaluator_criteria)
        self.assertTrue(eligibility.eligible)
        self.assertEqual(eligibility.reasons_ineligible, {'none': 'None'})

    def test_eligibility_ok_by_literate_witness(self):
        criteria = copy(self.evaluator_criteria)
        criteria.update({'literate': False})
        criteria.update({'literate_witness_present': True})
        obj = Eligibility(**criteria)
        self.assertTrue(obj.eligible)

    def test_eligibility_ok_by_documents_present(self):
        criteria = copy(self.evaluator_criteria)
        criteria.update({'citizen': False})
        criteria.update({'married_to_citizen': True})
        criteria.update({'marriage_certificate_present': True})
        obj = Eligibility(**criteria)
        self.assertTrue(obj.eligible)

    def test_eligibility_ok_by_guardin_present(self):
        self.evaluator_criteria.update(age_in_years=16)
        self.evaluator_criteria.update(guardian_present=True)
        eligibility = Eligibility(**self.evaluator_criteria)
        self.assertTrue(eligibility.eligible)

    def test_eligibility_not_ok_by_age(self):
        self.evaluator_criteria.update(age_in_years=16)
        self.evaluator_criteria.update(guardian_present=False)
        eligibility = Eligibility(**self.evaluator_criteria)
        self.assertFalse(eligibility.eligible)

    def test_eligibility_not_ok_by_citizenship(self):
        self.evaluator_criteria.update(age_in_years=29)
        self.evaluator_criteria.update(citizen=False)
        self.evaluator_criteria.update(married_to_citizen=False)
        self.evaluator_criteria.update(marriage_certificate_present=False)
        eligibility = Eligibility(**self.evaluator_criteria)
        self.assertFalse(eligibility.eligible)

    def test_eligibility_not_ok_by_citizenship_and_documents_absent(self):
        self.evaluator_criteria.update(age_in_years=34)
        self.evaluator_criteria.update(citizen=False)
        self.evaluator_criteria.update(married_to_citizen=True)
        self.evaluator_criteria.update(marriage_certificate_present=False)
        eligibility = Eligibility(**self.evaluator_criteria)
        self.assertFalse(eligibility.eligible)

    def test_not_eligible_with_illiterate_reason(self):
        criteria = copy(self.evaluator_criteria)
        criteria.update({'literate': False})
        criteria.update({'literate_witness_present': False})
        obj = Eligibility(**criteria)
        self.assertFalse(obj.eligible)
        self.assertIn('literate', obj.reasons_ineligible)

    def test_not_eligible_with_minor_reasons(self):
        criteria = copy(self.evaluator_criteria)
        criteria.update({'age_in_years': 10})
        criteria.update({'guardian_present': False})
        obj = Eligibility(**criteria)
        self.assertFalse(obj.eligible)
        self.assertIn('minor', obj.reasons_ineligible)

    def test_not_eligible_with_citizenship_reasons(self):
        criteria = copy(self.evaluator_criteria)
        criteria.update({'citizen': False})
        criteria.update({'married_to_citizen': False})
        criteria.update({'marriage_certificate_present': False})
        obj = Eligibility(**criteria)
        self.assertFalse(obj.eligible)
        self.assertIn('citizen', obj.reasons_ineligible)

