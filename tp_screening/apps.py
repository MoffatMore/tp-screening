'''
Created on Jun 18, 2018

@author: moffat
'''
from django.apps import AppConfig as DjangoApponfig
from django.conf import settings
from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig


class AppConfig(DjangoApponfig):
    name = 'tp_screening'
    verbose_name = 'Training Program Subject Screening'
    screening_age_adult_upper = 99
    screening_age_adult_lower = 18