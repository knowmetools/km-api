"""URLs for the ``account`` module.
"""

from django.conf.urls import url

from account import views


urlpatterns = [
    url(r'^change-password/$', views.PasswordChangeView.as_view(), name='change-password'),     # noqa
    url(r'^profile/$', views.UserDetailView.as_view(), name='profile'),
]
