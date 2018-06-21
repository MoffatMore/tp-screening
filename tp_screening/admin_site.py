'''
Created on Jun 20, 2018

@author: moffat
'''
from django.contrib.admin import AdminSite as DjangoAdminSite
from django.contrib.sites.shortcuts import get_current_site


class MyAdminSite(DjangoAdminSite):

    site_url = '/administration/'

    def each_context(self, request):
        context = super().each_context(request)
        context.update(global_site=get_current_site(request))
        label = f'Trainee Project Subject Screening'
        context.update(
            site_title=label,
            site_header=label,
            index_title=label,
        )
        return context


tp_screening_admin = MyAdminSite(name='tp_screening_admin')
