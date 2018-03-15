from unittest import mock

from django.http import Http404

import pytest

from rest_framework.permissions import SAFE_METHODS

from know_me.journal import permissions


UNSAFE_METHODS = ("DELETE", "PATCH", "POST", "PUT")
ALL_METHODS = SAFE_METHODS + UNSAFE_METHODS


@pytest.mark.parametrize("method", ALL_METHODS)
@mock.patch(
    'know_me.journal.permissions.models.Entry.has_object_read_permission')
def test_has_permission(
        mock_read_permission,
        api_rf,
        method,
        entry_factory):
    """
    The permission check should be delegated to the entry whose comments
    are being listed.
    """
    entry = entry_factory()

    api_rf.user = entry.km_user.user
    request = api_rf.generic(method, '/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': entry.pk}

    permission = permissions.HasEntryCommentListPermissions()
    perm_func = mock_read_permission

    assert permission.has_permission(request, view) == perm_func.return_value
    assert perm_func.call_count == 1
    assert perm_func.call_args[0] == (request,)


def test_has_permission_nonexistent_entry(api_rf, db):
    """
    If there is no entry with the given ID, the permission check should
    raise an Http404 error.
    """
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': 1}

    permission = permissions.HasEntryCommentListPermissions()

    with pytest.raises(Http404):
        permission.has_permission(request, view)
