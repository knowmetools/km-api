from unittest import mock

from dry_rest_permissions.generics import DRYPermissions

import test_utils
from know_me.permissions import HasKMUserAccess, CollectionOwnerHasPremium
from know_me.profile import models, serializers, views


@mock.patch("know_me.profile.views.KMUserAccessFilterBackend.filter_queryset")
@mock.patch(
    "know_me.profile.views.filters.ProfileFilterBackend.filter_queryset"
)
def test_filter_queryset(mock_profile_filter, mock_access_filter):
    """
    The view should filter its queryset by passing it through the filter
    that restricts access to items based on the owner.
    """
    view = views.ProfileListView()
    view.request = None

    queryset = models.Profile.objects.none()

    view.filter_queryset(queryset)

    assert mock_access_filter.call_count == 1
    assert mock_profile_filter.call_count == 1


def test_get_permissions():
    """
    Test the permissions used by the view.
    """
    view = views.ProfileListView()

    assert test_utils.uses_permission_class(view, DRYPermissions)
    assert test_utils.uses_permission_class(view, HasKMUserAccess)
    assert test_utils.uses_permission_class(view, CollectionOwnerHasPremium)


def test_get_queryset(profile_factory):
    """
    The view should operate on all profiles.
    """
    profile_factory()
    profile_factory()
    profile_factory()

    view = views.ProfileListView()
    expected = models.Profile.objects.all()

    assert list(view.get_queryset()) == list(expected)


def test_get_serializer_class():
    """
    Test getting the serializer class the view uses.
    """
    view = views.ProfileListView()

    assert view.get_serializer_class() == serializers.ProfileListSerializer


def test_get_subscription_owner(km_user_factory):
    """
    The subscription owner for a profile collection should be the the
    owner of all the profiles.
    """
    km_user = km_user_factory()
    view = views.ProfileListView()
    view.kwargs = {"pk": km_user.pk}
    request = mock.Mock()

    assert view.get_subscription_owner(request) == km_user.user


def test_perform_create(km_user_factory):
    """
    When creating a new profile, it should be attached to the user
    specified in the URL.
    """
    km_user = km_user_factory()
    view = views.ProfileListView()
    view.kwargs = {"pk": km_user.pk}

    serializer = mock.Mock(name="Mock ProfileListSerializer")

    result = view.perform_create(serializer)

    assert result == serializer.save.return_value
    assert serializer.save.call_count == 1
    assert serializer.save.call_args[1] == {"km_user": km_user}
