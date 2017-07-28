"""URLs for the ``know_me`` module.
"""

from django.conf.urls import url

from know_me import views


urlpatterns = [
    url(r'^media-resources/(?P<pk>[0-9]+)/$', views.MediaResourceDetailView.as_view(), name='media-resource-detail'), # noqa
    url(r'^groups/(?P<pk>[0-9]+)/$', views.ProfileGroupDetailView.as_view(), name='profile-group-detail'),          # noqa
    url(r'^groups/(?P<pk>[0-9]+)/rows/$', views.ProfileRowListView.as_view(), name='profile-row-list'),             # noqa
    url(r'^items/(?P<pk>[0-9]+)/$', views.ProfileItemDetailView.as_view(), name='profile-item-detail'),             # noqa
    url(r'^profiles/$', views.ProfileListView.as_view(), name='profile-list'),
    url(r'^profiles/(?P<pk>[0-9])/$', views.ProfileDetailView.as_view(), name='profile-detail'),                    # noqa
    url(r'^profiles/(?P<pk>[0-9])/gallery/$', views.GalleryView.as_view(), name='gallery'),                         # noqa
    url(r'^profiles/(?P<pk>[0-9])/groups/$', views.ProfileGroupListView.as_view(), name='profile-group-list'),      # noqa
    url(r'^rows/(?P<pk>[0-9]+)/$', views.ProfileRowDetailView.as_view(), name='profile-row-detail'),                # noqa
    url(r'^rows/(?P<pk>[0-9]+)/items/$' ,views.ProfileItemListView.as_view(), name='profile-item-list'),            # noqa
]
