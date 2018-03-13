from django.conf.urls import url

from know_me.journal import views


app_name = 'journal'


urlpatterns = [
    url(
        r'^journal-entries/(?P<pk>[0-9]+)/$',
        views.EntryDetailView.as_view(),
        name='entry-detail'),

    url(
        r'^journal-entries/(?P<pk>[0-9]+)/comments/$',
        views.EntryCommentListView.as_view(),
        name='entry-comment-list'),

    url(
        r'^users/(?P<pk>[0-9]+)/journal-entries/$',
        views.EntryListView.as_view(),
        name='entry-list'),
]
