'''
Created on Jun 18, 2018

@author: moffat
'''

from edc_constants.constants import YES, NO


class CitizenEvaluator:
    """"""

    def __init__(self, citizen=None, married_to_citizen=False,
                 documents_present=None):
        self.eligible = False