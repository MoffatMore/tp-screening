from edc_constants.constants import YES, NO, NOT_APPLICABLE
from edc_form_validators import FormValidator


class SubjectScreeningFormValidator(FormValidator):

    def clean(self):
        condition = (self.cleaned_data.get('age_in_years') > 18)
        self.not_required_if(condition=condition, field='age_in_years',
                             field_required='guardian_present')

        condition = (self.cleaned_data.get('age_in_years') < 18)
        self.required_if_true(condition=condition, field='age_in_years',
                              field_required='guardian_present')

        self.not_applicable_if(NOT_APPLICABLE, NO, field='married_to_citizen',
                               field_applicable='documents_present')

        self.not_applicable_if(YES, field='citizen',
                               field_applicable='married_to_citizen')

        self.not_applicable_if(YES, field='literate',
                               field_applicable='witness_available')

        self.applicable_if(YES, field='married_to_citizen',
                           field_applicable='documents_present')
