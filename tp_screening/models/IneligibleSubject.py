'''
Created on Jun 21, 2018

@author: moffat
'''
from django.db import models
from edc_base.sites import CurrentSiteManager, SiteModelMixin

from django.utils import timezone


class IneligibleSubject(SiteModelMixin):

    screening_identifier = models.CharField(
        verbose_name='Screening ID',
        blank=True,
        max_length=50)

    report_datetime = models.DateTimeField(
        verbose_name='IneligibleSubject Enrollment Date & Time',
        default=timezone.now,
        help_text='Date and time of enrollment.')

    reasons_ineligible = models.TextField(
        verbose_name='Reason not eligible',
        max_length=150,
        default=None,
        null=True)

    def __str__(self):
        return f"""SID - {self.screening_identifier}
                    | Reasons Ineligible - {self.reasons_ineligible}"""
