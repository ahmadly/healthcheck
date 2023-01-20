from django.conf import settings
from django.urls import path
from django.utils.module_loading import import_string

view = getattr(settings, 'HEALTH_CHECK_VIEW', 'healthcheck.views.HealthCheckView')

urlpatterns = [
    path('', import_string(view).as_view(), name='healthcheck'),
]
