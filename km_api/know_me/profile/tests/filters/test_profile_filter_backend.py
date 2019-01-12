from unittest import mock

from know_me.profile import filters, models


def test_filter_queryset_owner(api_rf, km_user_factory, profile_factory):
    """
    All profiles should be included for requests by the owner.
    """
    km_user = km_user_factory()
    profile_factory(is_private=False, km_user=km_user)
    profile_factory(is_private=True, km_user=km_user)

    api_rf.user = km_user.user
    request = api_rf.get("/")

    view = mock.Mock(name="Mock View")
    view.kwargs = {"pk": km_user.pk}

    backend = filters.ProfileFilterBackend()
    result = backend.filter_queryset(
        request, models.Profile.objects.all(), view
    )

    expected = km_user.profiles.all()

    assert list(result) == list(expected)


def test_filter_queryset_shared_admin(
    api_rf, km_user_accessor_factory, km_user_factory, profile_factory
):
    """
    If the shared user is an admin, they should be able to see private
    profiles.
    """
    km_user = km_user_factory()
    accessor = km_user_accessor_factory(
        is_accepted=True, is_admin=True, km_user=km_user
    )

    profile_factory(is_private=False, km_user=km_user)
    profile_factory(is_private=True, km_user=km_user)

    api_rf.user = accessor.user_with_access
    request = api_rf.get("/")

    view = mock.Mock(name="Mock View")
    view.kwargs = {"pk": km_user.pk}

    backend = filters.ProfileFilterBackend()
    result = backend.filter_queryset(
        request, models.Profile.objects.all(), view
    )

    expected = km_user.profiles.all()

    assert list(result) == list(expected)


def test_filter_queryset_shared_non_admin(
    api_rf, km_user_accessor_factory, km_user_factory, profile_factory
):
    """
    If the shared user does not have admin permissions, private profiles
    should not be included in the results.
    """
    km_user = km_user_factory()
    accessor = km_user_accessor_factory(
        is_accepted=True, is_admin=False, km_user=km_user
    )

    profile_factory(is_private=False, km_user=km_user)
    profile_factory(is_private=True, km_user=km_user)

    api_rf.user = accessor.user_with_access
    request = api_rf.get("/")

    view = mock.Mock(name="Mock View")
    view.kwargs = {"pk": km_user.pk}

    backend = filters.ProfileFilterBackend()
    result = backend.filter_queryset(
        request, models.Profile.objects.all(), view
    )

    expected = km_user.profiles.filter(is_private=False)

    assert list(result) == list(expected)
