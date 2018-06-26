'''
Created on Jun 26, 2018

@author: moffat
'''
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .in_eligible_subject import IneligibleSubject
from .subject_screening import SubjectScreening


@receiver(post_save, sender=SubjectScreening)
def subject_screening_on_post_save(sender, instance, **kwargs):
    """Creates an enrollment loss instance for this screened subject, if
    eligibility fails.
    """
    if not instance.eligible:
        enrollment_loss_model = IneligibleSubject.objects.create(
            screening_identifier=instance.screening_identifier,
            report_datetime=instance.report_datetime,
            reasons_ineligible=instance.reasons_ineligible)
        enrollment_loss_model.save()


@receiver(post_delete, sender=SubjectScreening)
def model_post_delete(sender, instance, **kwargs):
    """Deletes all past records if enrollment loss"""
    IneligibleSubject.objects.filter(
        screening_identifier=instance.screening_identifier).delete()

