"""URLs for the ``account`` module.
"""

from django.conf.urls import url

from account import views


app_name = "account"


urlpatterns = [
    url(r"^profile/$", views.UserDetailView.as_view(), name="profile"),
    url(r"^users/$", views.UserListView.as_view(), name="user-list"),
]
