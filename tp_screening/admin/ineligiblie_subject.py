'''
Created on Jun 21, 2018

@author: moffat
'''
from django.contrib import admin

from ..models import IneligibleSubject
from ..admin_site import tp_screening_admin


class ChoiceInline(admin.TabularInline):
    model = IneligibleSubject


@admin.register(IneligibleSubject, site=tp_screening_admin)
class EnrollmentLossAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Screening Ineligible Subject Enrollment', {
            'fields': ('screening_identifier',
                       'report_datetime',
                       'reasons_ineligible'),
        }),
    )

    list_display = ('screening_identifier', 'report_datetime',
                    'reasons_ineligible')

    readonly_fields = ('screening_identifier',
                       'reasons_ineligible',)


admin.site.register(IneligibleSubject, EnrollmentLossAdmin)
