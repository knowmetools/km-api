"""URLs for the ``account`` module.
"""

from django.conf.urls import url

from account import views


urlpatterns = [
    url(r'^change-password/$', views.PasswordChangeView.as_view(), name='change-password'),     # noqa
    url(r'^emails/$', views.EmailListView.as_view(), name='email-list'),
    url(r'^emails/actions/$', views.EmailActionListView.as_view(), name='email-action-list'),   # noqa
    url(r'^emails/(?P<pk>[0-9]+)/$', views.EmailDetailView.as_view(), name='email-detail'),     # noqa
    url(r'^profile/$', views.UserDetailView.as_view(), name='profile'),
    url(r'^reset-password/$', views.PasswordResetView.as_view(), name='reset-password'),        # noqa
    url(r'^verify-email/$', views.EmailVerificationView.as_view(), name='verify-email'),        # noqa
]
