'''
Created on Jun 18, 2018

@author: moffat
'''


class CitizenEvaluator:
    """
    Participant must be a citizen
    Otherwise must be married to a citizen and have proof
    """

    def __init__(self, citizen=None, married_to_citizen=False,
                 documents_present=None):
        self.eligible = False
        self.reason_ineligible = None
        if citizen:
                self.eligible = True
        elif not citizen and married_to_citizen and documents_present:
            self.eligible = True

        if not self.eligible:
            self.reason_ineligible = []
            if not married_to_citizen:
                self.reason_ineligible.append('Subject not married to citizen')
            elif married_to_citizen and not documents_present:
                self.reason_ineligible.append('No proof of marriage certificate')