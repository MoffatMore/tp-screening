'''
Created on Jun 18, 2018

@author: moffat
'''
from edc_constants.constants import NORMAL, YES, NO

from .eligibility import Eligibility


def if_yes(value):
    if value == NORMAL:
        return True
    return value == YES


def if_no(value):
    return value == NO


def if_normal(value):
    return value == NORMAL


class SubjectScreeningEligibility:

    eligibility_cls = Eligibility

    def __init__(self, model_obj=None, allow_none=None):
        eligibility_obj = self.eligibility_cls(
            allow_none=allow_none,
            age=model_obj.age_in_years,
            gender=model_obj.gender,
            consent_ability=if_yes(model_obj.consent_ability),
            subject_screening=model_obj,
        )
        self.eligible = eligibility_obj.eligible
        self.reasons_ineligible = eligibility_obj.reasons_ineligible
