from rest_framework.reverse import reverse

from know_me import views


url = reverse("know-me:km-user-list")


def test_get_queryset_duplicates(
    api_rf, km_user_accessor_factory, km_user_factory, user_factory
):
    """
    If the user has managed to create an accessor granting access to
    their own account, there should not be a duplicate entry in the user
    list.

    Regression test for #352.
    """
    user = user_factory()
    api_rf.user = user

    km_user = km_user_factory(user=user)
    km_user_accessor_factory(
        is_accepted=True, km_user=km_user, user_with_access=user
    )

    # Have to create another accessor for the bug to be present
    km_user_accessor_factory(km_user=km_user)

    view = views.KMUserListView()
    view.request = api_rf.get("/")

    assert list(view.get_queryset()) == [km_user]


def test_get_queryset_order(
    api_rf, km_user_accessor_factory, km_user_factory, user_factory
):
    """
    The list of Know Me users should have the requesting user's Know Me
    user listed first, followed by any shared users.
    """
    user = user_factory()
    api_rf.user = user

    k1 = km_user_factory(user__has_premium=True)
    km_user_accessor_factory(
        is_accepted=True, km_user=k1, user_with_access=user
    )

    k2 = km_user_factory(user=user)

    k3 = km_user_factory(user__has_premium=True)
    km_user_accessor_factory(
        is_accepted=True, km_user=k3, user_with_access=user
    )

    view = views.KMUserListView()
    view.request = api_rf.get(url)

    expected = [k2, k1, k3]

    assert list(view.get_queryset()) == expected


def test_get_queryset_shared(api_rf, km_user_accessor_factory, user_factory):
    """
    If the requesting user is granted access to another Know Me user via
    an accessor and the owner of the other user has an active premium
    subscription, then the Know Me user should be included in the view's
    queryset.
    """
    user = user_factory()
    api_rf.user = user

    accessor = km_user_accessor_factory(
        is_accepted=True,
        km_user__user__has_premium=True,
        user_with_access=user,
    )

    view = views.KMUserListView()
    view.request = api_rf.get(url)

    assert list(view.get_queryset()) == [accessor.km_user]


def test_get_queryset_shared_not_accepted(
    api_rf, km_user_accessor_factory, user_factory
):
    """
    If the requesting user is granted access to another Know Me user via
    an accessor that they have not accepted, then the Know Me user
    should not be present in the queryset.
    """
    user = user_factory()
    api_rf.user = user

    km_user_accessor_factory(
        is_accepted=False,
        km_user__user__has_premium=True,
        user_with_access=user,
    )

    view = views.KMUserListView()
    view.request = api_rf.get(url)

    assert len(view.get_queryset()) == 0


def test_get_queryset_shared_without_premium(
    api_rf, km_user_accessor_factory, user_factory
):
    """
    If the requesting user is granted access to another Know Me user
    through an accessor but the other user does not have an active
    premium subscription, they should not be included in the queryset.
    """
    user = user_factory()
    api_rf.user = user

    km_user_accessor_factory(
        is_accepted=True,
        km_user__user__has_premium=False,
        user_with_access=user,
    )

    view = views.KMUserListView()
    view.request = api_rf.get(url)

    assert list(view.get_queryset()) == []
