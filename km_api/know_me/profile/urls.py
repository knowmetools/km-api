from django.conf.urls import include, url

from know_me.profile import views


app_name = "profile"


profile_urls = [
    url(
        r"^list-entries/(?P<pk>[0-9]+)/$",
        views.ListEntryDetailView.as_view(),
        name="list-entry-detail",
    ),
    url(
        r"^media-resource-categories/(?P<pk>[0-9]+)/$",
        views.MediaResourceCategoryDetailView.as_view(),
        name="media-resource-category-detail",
    ),
    url(
        r"^media-resources/(?P<pk>[0-9]+)/$",
        views.MediaResourceDetailView.as_view(),
        name="media-resource-detail",
    ),
    url(
        r"^profile-items/(?P<pk>[0-9]+)/$",
        views.ProfileItemDetailView.as_view(),
        name="profile-item-detail",
    ),
    url(
        r"^profile-items/(?P<pk>[0-9]+)/list-entries/$",
        views.ListEntryListView.as_view(),
        name="list-entry-list",
    ),
    url(
        r"^profile-topics/(?P<pk>[0-9]+)/$",
        views.ProfileTopicDetailView.as_view(),
        name="profile-topic-detail",
    ),
    url(
        r"^profile-topics/(?P<pk>[0-9]+)/items/$",
        views.ProfileItemListView.as_view(),
        name="profile-item-list",
    ),
    url(
        r"^profiles/(?P<pk>[0-9]+)/$",
        views.ProfileDetailView.as_view(),
        name="profile-detail",
    ),
    url(
        r"^profiles/(?P<pk>[0-9]+)/topics/$",
        views.ProfileTopicListView.as_view(),
        name="profile-topic-list",
    ),
]


user_detail_urls = [
    url(
        r"^media-resource-categories/$",
        views.MediaResourceCategoryListView.as_view(),
        name="media-resource-category-list",
    ),
    url(
        r"^media-resources/$",
        views.MediaResourceListView.as_view(),
        name="media-resource-list",
    ),
    url(r"^profiles/$", views.ProfileListView.as_view(), name="profile-list"),
]


urlpatterns = [
    url(r"^profile/", include(profile_urls)),
    url(r"^users/(?P<pk>[0-9]+)/", include(user_detail_urls)),
]
