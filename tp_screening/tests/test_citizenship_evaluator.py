'''
Created on Jun 18, 2018

@author: moffat
'''

from django.test import TestCase, tag
from ..citizenship_evaluator import CitizenEvaluator


class TestCitizenShip(TestCase):

        """Participant test if is a not citizen """

        @tag('citizen_not_eligible')
        def test_citizen_not_eligible(self):
            citizen = CitizenEvaluator(married_to_citizen=True,
                                       documents_present=False)
            self.assertFalse(citizen.eligible)
            citizen = CitizenEvaluator(married_to_citizen=False,
                                       documents_present=False)
            self.assertFalse(citizen.eligible)

        """Participant test if is a citizen """

        @tag('citizen_eligible')
        def test_citizen_eligible(self):
            citizen = CitizenEvaluator(citizen=True)
            self.assertTrue(citizen.eligible)
            citizen = CitizenEvaluator(citizen=True, married_to_citizen=True,
                                       documents_present=True)
            self.assertTrue(citizen.eligible)
            citizen = CitizenEvaluator(citizen=False, married_to_citizen=True,
                                       documents_present=True)
            self.assertTrue(citizen.eligible)

