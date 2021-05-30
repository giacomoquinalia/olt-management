from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('huawei/', include('apps.huawei.urls')),
    path('authentication_token/', obtain_auth_token, name='authentication_token'),
]
 