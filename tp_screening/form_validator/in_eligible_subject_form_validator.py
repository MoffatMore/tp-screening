'''
Created on Jun 21, 2018

@author: moffat
'''
from django import forms
from edc_form_validators import FormValidator


class IneligibleSubjectFormValidator(FormValidator):

    def clean(self):

        self.screening_identifier = self.cleaned_data.get('screening_identifier')
        self.reasons_ineligible = self.cleaned_data.get('reasons_ineligible')

        self.required_if_true(
            True, field_required='screening_identifier')

        self.required_if_true(
            True, field_required='reasons_ineligible')
