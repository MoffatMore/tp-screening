from django.urls.conf import path
from django.views.generic.base import RedirectView

from .admin_site import tp_screening_admin

app_name = 'tp_screening'

urlpatterns = [
    path('admin/', tp_screening_admin.urls),
    path('', RedirectView.as_view(url='/'), name='home_url'),
]
