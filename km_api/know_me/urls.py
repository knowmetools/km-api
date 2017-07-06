"""URLs for the ``know_me`` module.
"""

from django.conf.urls import include, url

from know_me import views


urlpatterns = [
    url(r'^items/(?P<pk>[0-9]+)/$', views.ProfileItemDetailView.as_view(), name='profile-item-detail'),                         # noqa
    url(r'^profiles/', include([
        url(r'^$', views.ProfileListView.as_view(), name='profile-list'),
        url(r'^(?P<profile_pk>[0-9]+)/', include([
            url(r'^$', views.ProfileDetailView.as_view(), name='profile-detail'),                                               # noqa
            url(r'^gallery/', include([
                url(r'^$', views.GalleryView.as_view(), name='gallery'),
                url(r'^(?P<gallery_item_pk>[0-9]+)/$', views.GalleryItemDetailView.as_view(), name='gallery-item-detail'),      # noqa
            ])),
            url(r'^groups/$', views.ProfileGroupListView.as_view(), name='profile-group-list'),                                 # noqa
            url(r'^groups/(?P<group_pk>[0-9]+)/', include([
                url(r'^$', views.ProfileGroupDetailView.as_view(), name='profile-group-detail'),                                # noqa
                url(r'^rows/', include([
                    url(r'^$', views.ProfileRowListView.as_view(), name='profile-row-list'),                                    # noqa
                    url(r'^(?P<row_pk>[0-9]+)/', include([
                        url(r'^$', views.ProfileRowDetailView.as_view(), name='profile-row-detail'),                            # noqa
                        url(r'^items/$', views.ProfileItemListView.as_view(), name='profile-item-list'),                          # noqa
                    ])),
                ])),
            ])),
            url(r'^teamtalk/', include('know_me.teamtalk.urls', namespace='teamtalk')),                                         # noqa
        ])),
    ])),
]
