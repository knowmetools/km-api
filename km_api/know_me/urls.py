"""URLs for the ``know_me`` module.
"""

from django.conf.urls import include, url

from know_me import views


urlpatterns = [
    url(r'^', include('know_me.journal.urls')),
    url(r'^', include('know_me.profile.urls')),

    url(
        r'^accessors/pending/$',
        views.PendingAccessorListView.as_view(),
        name='pending-accessor-list'),

    url(
        r'^accessors/(?P<pk>[0-9]+)/$',
        views.AccessorDetailView.as_view(),
        name='accessor-detail'),

    url(
        r'^users/$',
        views.KMUserListView.as_view(),
        name='km-user-list'),

    url(
        r'^users/accessors/$',
        views.AccessorListView.as_view(),
        name='accessor-list'),

    url(
        r'^users/(?P<pk>[0-9]+)/$',
        views.KMUserDetailView.as_view(),
        name='km-user-detail'),
]
