'''
Created on Jun 18, 2018

@author: moffat
'''
from django.test import TestCase, tag
from ..literacy_evaluator import LiteracyEvaluator


class LiteracyEvaluator(TestCase):

    '''
    Participant is eligible if and only if they are literate
    or have some witness'''
    @tag('literate')
    def test_participant_literate(self):
        literacy_evaluator = LiteracyEvaluator(literate=True)
        self.assertTrue(literacy_evaluator.eligible)