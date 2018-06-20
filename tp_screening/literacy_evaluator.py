'''
Created on Jun 18, 2018

@author: moffat
'''


class LiteracyEvaluator:

    """
    Participants are eligible if they are literate
    or have witness available
    """
    def __init__(self, literate=None, witness_present=False):
        self.eligible = None
        self.reasons_ineligible = None
        if literate:
            self.eligible = True
        elif not literate and witness_present:
            self.eligible = True
