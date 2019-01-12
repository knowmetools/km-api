from django.conf.urls import include, url

from know_me.journal import views


app_name = "journal"


journal_urls = [
    url(
        r"^comments/(?P<pk>[0-9]+)/$",
        views.EntryCommentDetailView.as_view(),
        name="entry-comment-detail",
    ),
    url(
        r"^entries/(?P<pk>[0-9]+)/$",
        views.EntryDetailView.as_view(),
        name="entry-detail",
    ),
    url(
        r"^entries/(?P<pk>[0-9]+)/comments/$",
        views.EntryCommentListView.as_view(),
        name="entry-comment-list",
    ),
]


urlpatterns = [
    url(r"^journal/", include(journal_urls)),
    url(
        r"^users/(?P<pk>[0-9]+)/journal-entries/$",
        views.EntryListView.as_view(),
        name="entry-list",
    ),
]
