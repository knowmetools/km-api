from django.conf.urls import url

from know_me.journal import views


app_name = 'journal'


urlpatterns = [
    url(
        r'^users/(?P<pk>[0-9]+)/journal-entries/$',
        views.EntryListView.as_view(),
        name='entry-detail'),
]
