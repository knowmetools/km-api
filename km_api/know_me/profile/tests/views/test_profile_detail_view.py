from unittest import mock

from dry_rest_permissions.generics import DRYPermissions

import test_utils
from know_me.permissions import ObjectOwnerHasPremium
from know_me.profile import models, serializers, views


def test_get_permissions():
    """
    Test the permissions used by the view.
    """
    view = views.ProfileDetailView()

    assert test_utils.uses_permission_class(view, DRYPermissions)
    assert test_utils.uses_permission_class(view, ObjectOwnerHasPremium)


def test_get_queryset(profile_factory):
    """
    The view should operate on all profiles.
    """
    profile_factory()
    profile_factory()
    profile_factory()

    view = views.ProfileDetailView()
    expected = models.Profile.objects.all()

    assert list(view.get_queryset()) == list(expected)


def test_get_serializer_class():
    """
    Test the serializer class used by the view.
    """
    view = views.ProfileDetailView()

    assert view.get_serializer_class() == serializers.ProfileDetailSerializer


def test_get_subscription_owner():
    """
    The subscription owner for a profile should be the profile's owner.
    """
    view = views.ProfileDetailView()
    request = mock.Mock()
    profile = mock.Mock()

    expected = profile.km_user.user

    assert view.get_subscription_owner(request, profile) == expected
