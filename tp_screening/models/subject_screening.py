'''
Created on Jun 15, 2018

@author: moffat
'''

import re
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager, SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import GENDER, YES_NO, YES_NO_NA
from edc_constants.constants import UUID_PATTERN
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_search.model_mixins import SearchSlugManager, SearchSlugModelMixin
from uuid import uuid4
from dateutil.relativedelta import relativedelta
from ..screening_identifier import ScreeningIdentifier
from ..subject_screening_eligibility import SubjectScreeningEligibility


class SubjectScreeningManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, screening_identifier):
        return self.get(screening_identifier=screening_identifier)


class SubjectIdentifierModelMixin(NonUniqueSubjectIdentifierModelMixin,
                                  SearchSlugModelMixin, models.Model):

    def update_subject_identifier_on_save(self):
        """Overridden to not set the subject identifier on save.
        """
        if not self.subject_identifier:
            self.subject_identifier = self.subject_identifier_as_pk.hex
        elif re.match(UUID_PATTERN, self.subject_identifier):
            pass
        return self.subject_identifier

    def make_new_identifier(self):
        return self.subject_identifier_as_pk.hex

    class Meta:
        abstract = True


class SubjectScreening(SubjectIdentifierModelMixin, SiteModelMixin, BaseUuidModel):

    eligibility_cls = SubjectScreeningEligibility

    identifier_cls = ScreeningIdentifier

    screening_identifier = models.CharField(
        verbose_name='Screening ID',
        max_length=50,
        blank=True,
        unique=True,
        editable=False)

    report_datetime = models.DateTimeField(
        verbose_name='Report Date and Time',
        default=get_utcnow,
        help_text='Date and time of report.')

    gender = models.CharField(
        choices=GENDER,
        max_length=10)

    age_in_years = models.IntegerField()

    citizen = models.CharField(
        max_length=10,
        choices=YES_NO_NA)

    married_to_citizen = models.CharField(
        max_length=5,
        choices=YES_NO_NA)

    documents_present = models.CharField(
        max_length=5,
        choices=YES_NO)

    literate = models.CharField(
        max_length=10,
        choices=YES_NO_NA)

    consent_ability = models.CharField(
        verbose_name='Participant or legal guardian/representative able and '
                     'willing to give informed consent.',
        max_length=5,
        choices=YES_NO_NA)

    eligible = models.BooleanField(
        default=False,
        editable=False)

    reasons_ineligible = models.TextField(
        verbose_name='Reason not eligible',
        max_length=150,
        null=True,
        editable=False)

    consented = models.BooleanField(
        default=False,
        editable=False)

    on_site = CurrentSiteManager()

    objects = SubjectScreeningManager()

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.screening_identifier} {self.gender} {self.age_in_years}'

    def save(self, *args, **kwargs):
        eligibility_obj = self.eligibility_cls(model_obj=self, allow_none=True)
        self.eligible = eligibility_obj.eligible
        if not self.eligible:
            reasons_ineligible = [
                v for v in eligibility_obj.reasons_ineligible.values() if v]
            reasons_ineligible.sort()
            self.reasons_ineligible = ','.join(reasons_ineligible)
        else:
            self.reasons_ineligible = None
        if not self.id:
            self.screening_identifier = self.identifier_cls().identifier
        super().save(*args, **kwargs)

    def natural_key(self):
        return (self.screening_identifier,)

    natural_key.dependencies = ['sites.Site']

    def get_search_slug_fields(self):
        return ['screening_identifier', 'subject_identifier', 'reference']

    @property
    def estimated_dob(self):
        return get_utcnow().date() - relativedelta(years=self.age_in_years)
