'''
Created on Jun 18, 2018

@author: moffat
'''
from edc_reportable import AgeEvaluator, ValueBoundryError
from dateutil.relativedelta import relativedelta
from django.utils.timezone import localtime
from edc_base.utils import get_utcnow


class MyAgeEvaluator(AgeEvaluator):
    """
    Eligible Participants must have age greater than 18
    Otherwise minors should have guardian to be eligible"""

    def __init__(self, **kwargs):
            self.reasons_ineligible = None
            super().__init__(**kwargs)

    def age_eligible(self, age_in_years=None, guardian_present=False):
            eligible = False
            if age_in_years:
                try:
                    self.in_bounds_or_raise(age=age_in_years)
                except ValueBoundryError:
                    if not guardian_present:
                        self.reasons_ineligible = 'age < 18. and Guardian is absent'
                    else:
                        eligible = True
                else:
                    eligible = True
            return eligible

    def in_bounds_or_raise(self, age=None):
        self.reasons_ineligible = None
        dob = localtime(get_utcnow() - relativedelta(years=age)).date()
        age_units = 'years'
        report_datetime = localtime(get_utcnow())
        return super().in_bounds_or_raise(
            dob=dob, report_datetime=report_datetime, age_units=age_units)


age_evaluator = MyAgeEvaluator(
    age_lower=18,
    age_lower_inclusive=True)
