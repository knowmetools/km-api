"""URLs for authentication views.
"""

from django.conf.urls import url

from km_auth import views


urlpatterns = (
    url(r'^register/$', views.UserRegistrationView.as_view(), name='register'),
)
