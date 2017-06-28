"""URLs for authentication views.
"""

from django.conf.urls import url

from km_auth import views


urlpatterns = (
    url(r'^profile/$', views.UserDetailView.as_view(), name='user-detail'),
    url(r'^register/$', views.UserRegistrationView.as_view(), name='register'),
)
