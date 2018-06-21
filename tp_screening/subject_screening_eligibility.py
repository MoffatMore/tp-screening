'''
Created on Jun 18, 2018

@author: moffat
'''
from edc_constants.constants import NOT_APPLICABLE, YES, NO

from .eligibility import Eligibility


def if_yes(value):
    if value == 'Not applicable':
        return True
    return value == YES


def if_no(value):
    return value == NO


class SubjectScreeningEligibility:

    eligibility_cls = Eligibility

    def __init__(self, model_obj=None, allow_none=None):
        eligibility_obj = self.eligibility_cls(
            age_in_years=model_obj.age_in_years,
            guardian_present=if_yes(model_obj.guardian_present),
            marriage_certificate_present=if_yes(
                model_obj.marriage_certificate_present),
            literate=if_yes(model_obj.literate),
            citizen=if_yes(model_obj.citizen),
            married_to_citizen=if_yes(model_obj.married_to_citizen),
            literate_witness_present=if_yes(model_obj.literate_witness_present)
        )
        self.eligible = eligibility_obj.eligible
        self.reasons_ineligible = eligibility_obj.reasons_ineligible
