'''
Created on Jun 18, 2018

@author: moffat
'''
from django.test import TestCase, tag
from ..literacy_evaluator import LiteracyEvaluator


class TestLiteracyEvaluator(TestCase):

    '''
    Participant is eligible if and only if they are literate
    or have some witness'''

    @tag('literate_test')
    def test_participant_literate(self):
        literacy_evaluator = LiteracyEvaluator(literate=True)
        self.assertTrue(literacy_evaluator.eligible)
        literacy_evaluator = LiteracyEvaluator(witness_present=True)
        self.assertTrue(literacy_evaluator)

    @tag('illiterate_test')
    def test_participant_not_literate_and_no_witness(self):
        literacy_evaluator = LiteracyEvaluator(literate=False)
        self.assertFalse(literacy_evaluator.eligible)
        literacy_evaluator = LiteracyEvaluator(literate=False,
                                               witness_present=False)
        self.assertIn(literacy_evaluator.reasons_ineligible,
                      'Participant is illiterate and witness is absent')
