from unittest import mock

from django.http import Http404

import pytest

from rest_framework.permissions import SAFE_METHODS

from know_me.profile import permissions


UNSAFE_METHODS = ("DELETE", "PATCH", "POST", "PUT")
ALL_METHODS = SAFE_METHODS + UNSAFE_METHODS


@pytest.mark.parametrize("method", ALL_METHODS)
@mock.patch(
    "know_me.profile.permissions.models.Profile.has_object_write_permission"
)
@mock.patch(
    "know_me.profile.permissions.models.Profile.has_object_read_permission"
)
def test_has_permission(
    mock_read_permission,
    mock_write_permission,
    api_rf,
    method,
    profile_factory,
):
    """
    The permission check should be delegated to the profile whose topics
    are being listed.
    """
    profile = profile_factory()

    api_rf.user = profile.km_user.user
    request = api_rf.generic(method, "/")

    view = mock.Mock(name="Mock View")
    view.kwargs = {"pk": profile.pk}

    permission = permissions.HasProfileTopicListPermissions()

    if method in SAFE_METHODS:
        perm_func = mock_read_permission
    else:
        perm_func = mock_write_permission

    assert permission.has_permission(request, view) == perm_func.return_value
    assert perm_func.call_count == 1
    assert perm_func.call_args[0] == (request,)


def test_has_permission_nonexistent_profile(api_rf, db):
    """
    If there is no profile with the given ID, the permission check
    should raise an Http404 error.
    """
    request = api_rf.get("/")

    view = mock.Mock(name="Mock View")
    view.kwargs = {"pk": 1}

    permission = permissions.HasProfileTopicListPermissions()

    with pytest.raises(Http404):
        permission.has_permission(request, view)
