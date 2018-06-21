'''
Created on Jun 21, 2018

@author: moffat
'''
from django.contrib import admin

from ..models.subject_screening import SubjectScreening
from ..admin_site import tp_screening_admin
from ..forms import SubjectScreeningForm


class ChoiceInline(admin.TabularInline):
    model = SubjectScreening


@admin.register(SubjectScreening, site=tp_screening_admin)
class SubjectScreeningAdmin(admin.ModelAdmin):

    form = SubjectScreeningForm

    radio_fields = {"gender": admin.VERTICAL,
                    "guardian_present": admin.VERTICAL,
                    "citizen": admin.VERTICAL,
                    "married_to_citizen": admin.VERTICAL,
                    "marriage_certificate_present": admin.VERTICAL,
                    "literate": admin.VERTICAL,
                    "literate_witness_present": admin.VERTICAL,
                    }

    fieldsets = (
        ('Subject Screening', {
            'fields': ('report_datetime', 'gender', 'age_in_years',
                       'guardian_present', 'citizen',
                       'married_to_citizen',
                       'marriage_certificate_present', 'literate',
                       'literate_witness_present', 'consent_ability'),
        }),
    )

    list_display = ('screening_identifier', 'age_in_years',
                    'citizen', 'literate', 'eligible', 'reasons_ineligible')


admin.site.register(SubjectScreening, SubjectScreeningAdmin)

