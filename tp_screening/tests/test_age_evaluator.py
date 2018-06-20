'''
Created on Jun 18, 2018

@author: moffat
'''
from django.test import TestCase, tag
from ..age_evaluator import age_evaluator


class TestAgeEvaluator(TestCase):

    """
    Participant age >= 18 is eligible else guardian must be present
    Minors with no guardians are not eligible
    """
    @tag('valid_age_eligibility')
    def test_valid_age_in_years_eligibility(self):
        # age_evaluator = MyAgeEvaluator(10)
        self.assertTrue(age_evaluator.age_eligible(18), True)
        self.assertTrue(
            age_evaluator.age_eligible(
                age_in_years=10, guardian_present=True), True)

    """Participant age < 18 are in eligible"""
    @tag('invalid_age_eligibility')
    def test_invalid_age_in_years_ineligibility(self):
        self.assertFalse(age_evaluator.age_eligible(16), False)
        age_evaluator.age_eligible(age_in_years=10, guardian_present=False)
        self.assertIn('age < 18. and Guardian is absent',
                      age_evaluator.reasons_ineligible)
