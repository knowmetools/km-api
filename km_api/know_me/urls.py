"""URLs for the ``know_me`` module.
"""

from django.conf.urls import include, url

from know_me import views


profile_group_detail_urls = [
    url(r'^$', views.ProfileGroupDetailView.as_view(), name='profile-group-detail'),        # noqa
]

profile_detail_urls = [
    url(r'^$', views.ProfileDetailView.as_view(), name='profile-detail'),
    url(r'^groups/$', views.ProfileGroupListView.as_view(), name='profile-group-list'),     # noqa
    url(r'^groups/(?P<group_pk>[0-9]+)/', include(profile_group_detail_urls)),
]

profile_urls = [
    url(r'^$', views.ProfileListView.as_view(), name='profile-list'),
    url(r'^(?P<profile_pk>[0-9]+)/', include(profile_detail_urls)),
]


urlpatterns = [
    url(r'^profiles/', include(profile_urls)),
]
