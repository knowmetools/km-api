"""URLs for the ``know_me`` module.
"""

from django.conf.urls import url

from know_me import views


urlpatterns = [
    url(r'^media-resources/(?P<pk>[0-9]+)/$', views.MediaResourceDetailView.as_view(), name='media-resource-detail'), # noqa
    url(r'^groups/(?P<pk>[0-9]+)/$', views.ProfileGroupDetailView.as_view(), name='profile-group-detail'),          # noqa
    url(r'^groups/(?P<pk>[0-9]+)/topics/$', views.ProfileTopicListView.as_view(), name='profile-topic-list'),             # noqa
    url(r'^items/(?P<pk>[0-9]+)/$', views.ProfileItemDetailView.as_view(), name='profile-item-detail'),             # noqa
    url(r'^topics/(?P<pk>[0-9]+)/$', views.ProfileTopicDetailView.as_view(), name='profile-topic-detail'),                # noqa
    url(r'^topics/(?P<pk>[0-9]+)/items/$' ,views.ProfileItemListView.as_view(), name='profile-item-list'),            # noqa
    url(r'^users/$', views.KMUserListView.as_view(), name='km-user-list'),
    url(r'^users/(?P<pk>[0-9])/$', views.KMUserDetailView.as_view(), name='km-user-detail'),                    # noqa
    url(r'^users/(?P<pk>[0-9])/gallery/$', views.GalleryView.as_view(), name='gallery'),                         # noqa
    url(r'^users/(?P<pk>[0-9])/groups/$', views.ProfileGroupListView.as_view(), name='profile-group-list'),      # noqa
]
