"""URLs for the ``know_me`` module.
"""

from django.conf.urls import url

from know_me import views


urlpatterns = [
    url(r'^emergency-contacts/(?P<pk>[0-9]+)/$', views.EmergencyContactDetailView.as_view(), name='emergency-contact-detail'),      # noqa
    url(r'^emergency-items/(?P<pk>[0-9]+)/$', views.EmergencyItemDetailView.as_view(), name='emergency-item-detail'),               # noqa
    url(r'^media-resources/(?P<pk>[0-9]+)/$', views.MediaResourceDetailView.as_view(), name='media-resource-detail'),               # noqa
    url(r'^items/(?P<pk>[0-9]+)/$', views.ProfileItemDetailView.as_view(), name='profile-item-detail'),                             # noqa
    url(r'^profiles/(?P<pk>[0-9]+)/$', views.ProfileDetailView.as_view(), name='profile-detail'),                                   # noqa
    url(r'^profiles/(?P<pk>[0-9]+)/topics/$', views.ProfileTopicListView.as_view(), name='profile-topic-list'),                     # noqa
    url(r'^topics/(?P<pk>[0-9]+)/$', views.ProfileTopicDetailView.as_view(), name='profile-topic-detail'),                          # noqa
    url(r'^topics/(?P<pk>[0-9]+)/items/$' ,views.ProfileItemListView.as_view(), name='profile-item-list'),                          # noqa
    url(r'^users/$', views.KMUserListView.as_view(), name='km-user-list'),
    url(r'^users/(?P<pk>[0-9])/$', views.KMUserDetailView.as_view(), name='km-user-detail'),                                        # noqa
    url(r'^users/(?P<pk>[0-9]+)/emergency-contacts/$', views.EmergencyContactListView.as_view(), name='emergency-contact-list'),    # noqa
    url(r'^users/(?P<pk>[0-9])/emergency-items/$', views.EmergencyItemListView.as_view(), name='emergency-item-list'),              # noqa
    url(r'^users/(?P<pk>[0-9])/gallery/$', views.GalleryView.as_view(), name='gallery'),                                            # noqa
    url(r'^users/(?P<pk>[0-9])/profiles/$', views.ProfileListView.as_view(), name='profile-list'),                                  # noqa
]
