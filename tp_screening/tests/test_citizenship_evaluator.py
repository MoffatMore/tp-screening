'''
Created on Jun 18, 2018

@author: moffat
'''

from django.test import TestCase, tag
from ..citizenship_evaluator import CitizenEvaluator


class TestCitizenShip(TestCase):

        @tag('citizen_not_eligible')
        def test_citizen_not_eligible(self):
            citizen = CitizenEvaluator(citizen=True)
            self.assertTrue(citizen.eligible)
            pass
