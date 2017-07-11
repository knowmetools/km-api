"""URLs for authentication views.
"""

from django.conf.urls import url

from rest_framework.authtoken.views import obtain_auth_token

from km_auth import views


urlpatterns = (
    url(r'^layer/$', views.LayerIdentityView.as_view(), name='layer'),
    url(r'^login/$', obtain_auth_token, name='login'),
    url(r'^register/$', views.UserRegistrationView.as_view(), name='register'),
)
