'''
Created on Jun 18, 2018

@author: moffat
'''


from edc_constants.constants import YES, NO
from .citizenship_evaluator import CitizenEvaluator
from .literacy_evaluator import LiteracyEvaluator
from .age_evaluator import age_evaluator


def if_yes(value):
    return value == YES


def if_no(value):
    return value == NO


class EligibilityError(Exception):
    pass


class Eligibility:

    reasons_ineligible = {}

    """Eligible if all criteria evaluate True.

    Any key in `additional_criteria` has value True if eligible.
    """
    citizen_evaluator_cls = CitizenEvaluator
    literacy_evaluator_cls = LiteracyEvaluator
    age_evaluator = age_evaluator

    def __init__(self, age_in_years=None, guardian_present=None, citizen=None,
                 married_to_citizen=None, marriage_certificate_present=None,
                 literate=None, literate_witness_present=None):

        self.criteria = {}
        self.citizen_evaluator = self.citizen_evaluator_cls(
            citizen=citizen, married_to_citizen=married_to_citizen,
            documents_present=marriage_certificate_present)

        self.literacy_evaluator = self.literacy_evaluator_cls(
            literate=literate,
            witness_present=literate_witness_present)

        self.criteria.update(minor=self.age_evaluator.age_eligible(
            age_in_years=age_in_years, guardian_present=guardian_present))
        self.criteria.update(citizen=self.citizen_evaluator.eligible)
        self.criteria.update(literate=self.literacy_evaluator.eligible)

        self.eligible = all([v for v in self.criteria.values()])

        if self.eligible:
            self.reasons_ineligible = {'none': 'None'}
        else:
            self.reasons_ineligible = {
                k: v for k, v in self.criteria.items() if not v}
            for k, v in self.criteria.items():
                if not v:
                    if k in self.custom_reasons_dict:
                        self.reasons_ineligible.update(
                            {k: self.custom_reasons_dict.get(k)})
                    elif k not in ['minor', 'citizen', 'literate']:
                        self.reasons_ineligible.update({k: k})

            if not self.age_evaluator.age_eligible(age_in_years=age_in_years,
                                                   guardian_present=guardian_present):
                self.reasons_ineligible.update(
                    minor=self.age_evaluator.reasons_ineligible)

            if not self.citizen_evaluator.eligible:
                self.reasons_ineligible.update(
                    citizen=self.citizen_evaluator.reasons_ineligible)

            if not self.literacy_evaluator.eligible:
                self.reasons_ineligible.update(
                    literate=self.literacy_evaluator.reasons_ineligible)

    def __str__(self):
        return self.eligible

    @property
    def custom_reasons_dict(self):
        """Returns a dictionary of custom reasons for named criteria.
        """
        custom_reasons_dict = dict()
#             consent_ability='Not able or unwilling to give ICF')
        for k in custom_reasons_dict:
            if k in custom_reasons_dict and k not in self.criteria:
                raise EligibilityError(
                    f'''Custom reasons refer to invalid named criteria,
                    Got \'{k}\'. '''
                    f'Expected one of {list(self.criteria)}. '
                    f'See {repr(self)}.')
        return custom_reasons_dict
