"""URLs for the ``know_me`` module.
"""

from django.conf.urls import include, url

from know_me import views


urlpatterns = [
    url(r'^profiles/', include([
        url(r'^$', views.ProfileListView.as_view(), name='profile-list'),
        url(r'^(?P<profile_pk>[0-9]+)/', include([
            url(r'^$', views.ProfileDetailView.as_view(), name='profile-detail'),                                       # noqa
            url(r'^groups/$', views.ProfileGroupListView.as_view(), name='profile-group-list'),                         # noqa
            url(r'^groups/(?P<group_pk>[0-9]+)/', include([
                url(r'^$', views.ProfileGroupDetailView.as_view(), name='profile-group-detail'),                        # noqa
                url(r'^rows/', include([
                    url(r'^$', views.ProfileRowListView.as_view(), name='profile-row-list'),                            # noqa
                    url(r'^(?P<row_pk>[0-9]+)/$', views.ProfileRowDetailView.as_view(), name='profile-row-detail'),     # noqa
                ])),
            ])),
        ])),
    ])),
]
