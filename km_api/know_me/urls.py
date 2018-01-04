"""URLs for the ``know_me`` module.
"""

from django.conf.urls import include, url

from know_me import views


user_detail_endpoints = [
    url(
        r'^$',
        views.KMUserDetailView.as_view(),
        name='km-user-detail'),

    url(
        r'^media-resources/$',
        views.MediaResourceListView.as_view(),
        name='media-resource-list'),

    url(
        r'^profiles/$',
        views.ProfileListView.as_view(),
        name='profile-list'),
]


urlpatterns = [
    url(r'^accessors/pending/$', views.PendingAccessorListView.as_view(), name='pending-accessor-list'),                            # noqa
    url(r'^accessors/(?P<pk>[0-9]+)/$', views.AccessorDetailView.as_view(), name='accessor-detail'),                                # noqa
    url(r'^media-resources/(?P<pk>[0-9]+)/$', views.MediaResourceDetailView.as_view(), name='media-resource-detail'),               # noqa
    url(r'^items/(?P<pk>[0-9]+)/$', views.ProfileItemDetailView.as_view(), name='profile-item-detail'),                             # noqa
    url(r'^items/(?P<pk>[0-9]+)/list-entries/$', views.ListEntryListView.as_view(), name='list-entry-list'),                        # noqa
    url(r'^list-entries/(?P<pk>[0-9]+)/$', views.ListEntryDetailView.as_view(), name='list-entry-detail'),                          # noqa
    url(r'^profiles/(?P<pk>[0-9]+)/$', views.ProfileDetailView.as_view(), name='profile-detail'),                                   # noqa
    url(r'^profiles/(?P<pk>[0-9]+)/topics/$', views.ProfileTopicListView.as_view(), name='profile-topic-list'),                     # noqa
    url(r'^topics/(?P<pk>[0-9]+)/$', views.ProfileTopicDetailView.as_view(), name='profile-topic-detail'),                          # noqa
    url(r'^topics/(?P<pk>[0-9]+)/items/$' ,views.ProfileItemListView.as_view(), name='profile-item-list'),                          # noqa
    url(r'^users/$', views.KMUserListView.as_view(), name='km-user-list'),
    url(r'^users/accessors/$', views.AccessorListView.as_view(), name='accessor-list'),                                             # noqa
    url(r'^users/(?P<pk>[0-9]+)/', include(user_detail_endpoints)),
]
