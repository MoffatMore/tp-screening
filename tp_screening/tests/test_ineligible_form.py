'''
Created on Jun 26, 2018

@author: moffat
'''
from django.test import TestCase
from ..forms import IneligibleSubjectForm
from edc_base.utils import get_utcnow
from copy import copy


class TestInEligibleForm(TestCase):

    def setUp(self):
        self.enrollment_loss_data = dict(
            screening_identifier='S99IDGAF',
            report_datetime=get_utcnow(),
            reasons_ineligible='None')

    def test_default_ok(self):
        form = IneligibleSubjectForm(data=self.enrollment_loss_data)
        form.is_valid()
#         print(form.cleaned_data)
        self.assertEqual(form.errors, {})
        self.assertTrue(form.save())

    def test_no_reasons_ineligible(self):
        """test whether no reasons ineligible will raise and
        throw an error"""
        data = copy(self.enrollment_loss_data)
        data.update(reasons_ineligible=None)
        form = IneligibleSubjectForm(data=data)
        form.is_valid()
#         print(form.cleaned_data)
        self.assertEqual(
            form.errors, {'reasons_ineligible':
                          ['This field is required.']})

    def test_no_identifier(self):
        """test whether no screening identifier will raise and
        throw an error"""
        data = copy(self.enrollment_loss_data)
        data.update(screening_identifier=None)
        form = IneligibleSubjectForm(data=data)
        form.is_valid()
#         print(form.cleaned_data)
        self.assertEqual(
            form.errors, {'screening_identifier':
                          ['This field is required.']})
