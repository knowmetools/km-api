from unittest import mock

from django.http import Http404

import pytest

from rest_framework.permissions import SAFE_METHODS

from know_me.journal import permissions


UNSAFE_METHODS = ("DELETE", "PATCH", "POST", "PUT")
ALL_METHODS = SAFE_METHODS + UNSAFE_METHODS


@pytest.mark.parametrize("method", ALL_METHODS)
@mock.patch(
    "know_me.journal.permissions.models.Entry.has_object_read_permission"
)
def test_has_permission_active_subscription(
    mock_read_permission,
    api_rf,
    enable_premium_requirement,
    method,
    entry_factory,
):
    """
    The permission check should be delegated to the entry whose comments
    are being listed if the entry owner has an active premium
    subscription.
    """
    entry = entry_factory(km_user__user__has_premium=True)

    api_rf.user = entry.km_user.user
    request = api_rf.generic(method, "/")

    view = mock.Mock(name="Mock View")
    view.kwargs = {"pk": entry.pk}

    permission = permissions.HasEntryCommentListPermissions()
    perm_func = mock_read_permission

    assert permission.has_permission(request, view) == perm_func.return_value
    assert perm_func.call_count == 1
    assert perm_func.call_args[0] == (request,)


@pytest.mark.parametrize("has_premium", (True, False))
@pytest.mark.parametrize("method", ALL_METHODS)
@mock.patch(
    "know_me.journal.permissions.models.Entry.has_object_read_permission"
)
def test_has_permission_no_premium_check(
    mock_read_permission, api_rf, has_premium, method, entry_factory
):
    """
    If the journal entry exists and the premium check is disabled, the
    permission check should be delegated to the journal entry itself
    regardless of premium status.
    """
    entry = entry_factory(km_user__user__has_premium=has_premium)

    api_rf.user = entry.km_user.user
    request = api_rf.generic(method, "/")

    view = mock.Mock(name="Mock View")
    view.kwargs = {"pk": entry.pk}

    permission = permissions.HasEntryCommentListPermissions()
    perm_func = mock_read_permission

    assert permission.has_permission(request, view) == perm_func.return_value
    assert perm_func.call_count == 1
    assert perm_func.call_args[0] == (request,)


@pytest.mark.parametrize("method", ALL_METHODS)
def test_has_permission_no_subscription(
    api_rf, enable_premium_requirement, method, entry_factory
):
    """
    If the owner of the journal entry does not have an active premium
    subscription, a 404 error should be raised.
    """
    entry = entry_factory(km_user__user__has_premium=False)

    api_rf.user = entry.km_user.user
    request = api_rf.generic(method, "/")

    view = mock.Mock(name="Mock View")
    view.kwargs = {"pk": entry.pk}

    permission = permissions.HasEntryCommentListPermissions()

    with pytest.raises(Http404):
        permission.has_permission(request, view)


def test_has_permission_nonexistent_entry(api_rf, db):
    """
    If there is no entry with the given ID, the permission check should
    raise an Http404 error.
    """
    request = api_rf.get("/")

    view = mock.Mock(name="Mock View")
    view.kwargs = {"pk": 1}

    permission = permissions.HasEntryCommentListPermissions()

    with pytest.raises(Http404):
        permission.has_permission(request, view)
