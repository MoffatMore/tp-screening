'''
Created on Jun 18, 2018

@author: moffat
'''
from django.apps import AppConfig as DjangoApponfig


class AppConfig(DjangoApponfig):
    name = 'tp_screening'
    verbose_name = 'Training Program Subject Screening'
    screening_age_adult_upper = 99
    screening_age_adult_lower = 18

    def ready(self):
        pass
#         from .models.subject_rejection import subject_screening_on_post_save
