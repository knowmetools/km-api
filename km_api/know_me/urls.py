"""URLs for the ``know_me`` module.
"""

from django.conf.urls import url

from know_me import views


urlpatterns = (
    url(r'^profiles/$', views.ProfileListView.as_view(), name='profile-list'),
)
