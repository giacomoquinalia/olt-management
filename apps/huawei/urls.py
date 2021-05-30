from django.urls import path
from . import views


urlpatterns = [
    path('autofind', views.Autofind.as_view(), name='autofind'),
    path('provisioning', views.Provisioning.as_view(), name='provisioning'),
    path('unprovisioning', views.Unprovisioning.as_view(), name='unprovisioning'),
    path('custom', views.Customized.as_view(), name='custom'),
]