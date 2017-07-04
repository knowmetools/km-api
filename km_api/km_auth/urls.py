"""URLs for authentication views.
"""

from django.conf.urls import url

from rest_framework.authtoken.views import obtain_auth_token

from km_auth import views


urlpatterns = (
    url(r'^login/$', obtain_auth_token, name='login'),
    url(r'^profile/$', views.UserDetailView.as_view(), name='user-detail'),
    url(r'^register/$', views.UserRegistrationView.as_view(), name='register'),
)
