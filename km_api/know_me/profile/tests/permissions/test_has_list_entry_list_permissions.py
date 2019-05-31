from unittest import mock

import pytest
from django.http import Http404
from rest_framework.permissions import SAFE_METHODS

from know_me.profile import permissions


UNSAFE_METHODS = ("DELETE", "PATCH", "POST", "PUT")
ALL_METHODS = SAFE_METHODS + UNSAFE_METHODS


mock_has_object_read_permission = mock.patch(
    "know_me.profile.permissions.models.ProfileTopic.has_object_read_permission"  # noqa
)


@pytest.mark.parametrize("method", ALL_METHODS)
@mock.patch(
    "know_me.profile.permissions.models.ProfileTopic.has_object_write_permission"  # noqa
)
@mock_has_object_read_permission
def test_has_permission(
    mock_read_permission,
    mock_write_permission,
    api_rf,
    enable_premium_requirement,
    method,
    profile_item_factory,
):
    """
    The permission check should be delegated to the profile item whose
    list entries are being listed.
    """
    item = profile_item_factory(
        topic__profile__km_user__user__has_premium=True
    )

    api_rf.user = item.topic.profile.km_user.user
    request = api_rf.generic(method, "/")

    view = mock.Mock(name="Mock View")
    view.kwargs = {"pk": item.pk}

    permission = permissions.HasListEntryListPermissions()

    if method in SAFE_METHODS:
        perm_func = mock_read_permission
    else:
        perm_func = mock_write_permission

    assert permission.has_permission(request, view) == perm_func.return_value
    assert perm_func.call_count == 1
    assert perm_func.call_args[0] == (request,)


def test_has_permission_no_premium(
    api_rf, enable_premium_requirement, profile_item_factory
):
    """
    If the profile owner does not have an active premium subscription,
    an ``Http404`` exception should be raised.
    """
    item = profile_item_factory()

    api_rf.user = item.topic.profile.km_user.user
    request = api_rf.get("/")

    view = mock.Mock(name="Mock View")
    view.kwargs = {"pk": item.pk}

    permission = permissions.HasListEntryListPermissions()

    with pytest.raises(Http404):
        permission.has_permission(request, view)


def test_has_permission_nonexistent_item(api_rf, db):
    """
    If there is no profile item with the given ID, the permission check
    should raise an Http404 error.
    """
    request = api_rf.get("/")

    view = mock.Mock(name="Mock View")
    view.kwargs = {"pk": 1}

    permission = permissions.HasListEntryListPermissions()

    with pytest.raises(Http404):
        permission.has_permission(request, view)


@mock_has_object_read_permission
def test_has_permission_premium_disabled(
    mock_read_permission, api_rf, profile_item_factory
):
    """
    If the profile owner does not have a premium subscription but
    premium is not required, the permission check should be delegated to
    the profile item as usual.
    """
    item = profile_item_factory()

    api_rf.user = item.topic.profile.km_user.user
    request = api_rf.get("/")

    view = mock.Mock(name="Mock View")
    view.kwargs = {"pk": item.pk}

    permission = permissions.HasListEntryListPermissions()

    expected = mock_read_permission.return_value

    assert permission.has_permission(request, view) == expected
    assert mock_read_permission.call_args[0] == (request,)
