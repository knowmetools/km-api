"""URLs for the ``know_me`` module.
"""

from django.conf.urls import include, url
from django.urls import path

from know_me import views


app_name = "know-me"


urlpatterns = [
    url(r"^", include("know_me.journal.urls")),
    url(r"^", include("know_me.profile.urls")),
    url(
        r"^accessors/accepted/$",
        views.AcceptedAccessorListView.as_view(),
        name="accepted-accessor-list",
    ),
    url(
        r"^accessors/pending/$",
        views.PendingAccessorListView.as_view(),
        name="pending-accessor-list",
    ),
    url(
        r"^accessors/(?P<pk>[0-9]+)/$",
        views.AccessorDetailView.as_view(),
        name="accessor-detail",
    ),
    url(
        r"^accessors/(?P<pk>[0-9]+)/accept/$",
        views.AccessorAcceptView.as_view(),
        name="accessor-accept",
    ),
    url(r"^config/$", views.ConfigDetailView.as_view(), name="config-detail"),
    url(
        r"^legacy-users/$",
        views.LegacyUserListView.as_view(),
        name="legacy-user-list",
    ),
    url(
        r"^legacy-users/(?P<pk>[0-9]+)/$",
        views.LegacyUserDetailView.as_view(),
        name="legacy-user-detail",
    ),
    path(
        "subscription/",
        views.SubscriptionDetailView.as_view(),
        name="subscription-detail",
    ),
    path(
        "subscription/apple/",
        views.AppleSubscriptionView.as_view(),
        name="apple-subscription-detail",
    ),
    path(
        "subscription/apple/query/",
        views.AppleReceiptQueryView.as_view(),
        name="apple-receipt-query",
    ),
    path(
        "subscription/transfer/",
        views.SubscriptionTransferView.as_view(),
        name="subscription-transfer-create",
    ),
    url(r"^users/$", views.KMUserListView.as_view(), name="km-user-list"),
    url(
        r"^users/accessors/$",
        views.AccessorListView.as_view(),
        name="accessor-list",
    ),
    url(
        r"^users/(?P<pk>[0-9]+)/$",
        views.KMUserDetailView.as_view(),
        name="km-user-detail",
    ),
]
