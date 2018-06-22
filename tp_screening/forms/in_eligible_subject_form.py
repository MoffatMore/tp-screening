'''
Created on Jun 21, 2018

@author: moffat
'''
from django import forms
from edc_form_validators import FormValidatorMixin
from tp_screening.form_validator.in_eligible_subject_form_validator import IneligibleSubjectFormValidator

from ..models.in_eligible_subject import IneligibleSubject


class IneligibleSubjectForm(FormValidatorMixin, forms.ModelForm):

    form_validator_cls = IneligibleSubjectFormValidator

    class Meta:
        model = IneligibleSubject
        fields = '__all__'
