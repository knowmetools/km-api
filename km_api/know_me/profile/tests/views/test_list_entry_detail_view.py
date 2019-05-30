from unittest import mock

from dry_rest_permissions.generics import DRYPermissions

import test_utils
from know_me.permissions import ObjectOwnerHasPremium
from know_me.profile import models, serializers, views


def test_get_permissions():
    """
    Test the permissions used by the view.
    """
    view = views.ListEntryDetailView()

    assert test_utils.uses_permission_class(view, DRYPermissions)
    assert test_utils.uses_permission_class(view, ObjectOwnerHasPremium)


def test_get_queryset(list_entry_factory):
    """
    The view should operate on all list entries.
    """
    list_entry_factory()
    list_entry_factory()
    list_entry_factory()

    view = views.ListEntryDetailView()

    assert list(view.get_queryset()) == list(models.ListEntry.objects.all())


def test_get_serializer_class():
    """
    Test the serializer class the view uses.
    """
    view = views.ListEntryDetailView()
    expected = serializers.ListEntrySerializer

    assert view.get_serializer_class() == expected


def test_get_subscription_owner(profile_list_entry_factory):
    """
    The subscription owner should be the user who owns the profile that
    the list entry is contained in.
    """
    view = views.ListEntryDetailView()
    request = mock.Mock(name="Mock Request")
    entry = profile_list_entry_factory()

    expected = entry.profile_item.topic.profile.km_user.user

    assert view.get_subscription_owner(request, entry) == expected
