import pytest

from rest_framework.permissions import SAFE_METHODS

from account import permissions


UNSAFE_METHODS = ("DELETE", "PATCH", "POST", "PUT")
ALL_METHODS = SAFE_METHODS + UNSAFE_METHODS


@pytest.mark.parametrize("is_staff", [True, False])
@pytest.mark.parametrize("method", ALL_METHODS)
def test_has_permission(api_rf, is_staff, method, user_factory):
    """
    Staff users should be granted access for any request method.
    """
    user = user_factory(is_staff=is_staff)

    api_rf.user = user
    request = api_rf.generic(method, "/")

    permission = permissions.IsStaff()

    assert permission.has_permission(request, None) == is_staff


@pytest.mark.parametrize("method", ALL_METHODS)
def test_has_permission_unauthenticated(api_rf, method):
    """
    Unauthenticated users should not have permissions.
    """
    request = api_rf.generic(method, "/")
    permission = permissions.IsStaff()

    assert not permission.has_permission(request, None)
