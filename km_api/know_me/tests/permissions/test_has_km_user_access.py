from unittest import mock

from django.http import Http404

import pytest

from rest_framework.permissions import SAFE_METHODS

from know_me import permissions


UNSAFE_METHODS = ("DELETE", "PATCH", "POST", "PUT")
ALL_METHODS = SAFE_METHODS + UNSAFE_METHODS


def test_anonymous(api_rf, km_user_factory):
    """
    Anonymous users should not have access.
    """
    km_user = km_user_factory()

    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': km_user.pk}

    perm_instance = permissions.HasKMUserAccess()

    assert not perm_instance.has_permission(request, view)


@pytest.mark.parametrize("request_method", ALL_METHODS)
def test_is_user(api_rf, km_user_factory, request_method):
    """
    The user who owns the Know Me user should be granted access for any
    request method.
    """
    km_user = km_user_factory()
    api_rf.user = km_user.user

    request = api_rf.generic(request_method, '/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': km_user.pk}

    perm_instance = permissions.HasKMUserAccess()

    assert perm_instance.has_permission(request, view)


@pytest.mark.parametrize("request_method", ALL_METHODS)
def test_shared_admin(
        api_rf,
        km_user_accessor_factory,
        km_user_factory,
        request_method,
        user_factory):
    """
    A user who is granted write-access through an accessor should be
    granted access for any request method.
    """
    km_user = km_user_factory()
    user = user_factory()

    km_user_accessor_factory(
        is_accepted=True,
        is_admin=True,
        km_user=km_user,
        user_with_access=user)

    api_rf.user = user
    request = api_rf.generic(request_method, '/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': km_user.pk}

    perm_instance = permissions.HasKMUserAccess()

    assert perm_instance.has_permission(request, view)


@pytest.mark.parametrize("request_method", ALL_METHODS)
def test_shared_read_only(
        api_rf,
        km_user_accessor_factory,
        km_user_factory,
        request_method,
        user_factory):
    """
    If the user only has read-access from the accessor, only safe
    methods should be permitted.
    """
    km_user = km_user_factory()
    user = user_factory()

    km_user_accessor_factory(
        is_accepted=True,
        is_admin=False,
        km_user=km_user,
        user_with_access=user)

    api_rf.user = user
    request = api_rf.generic(request_method, '/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': km_user.pk}

    perm_instance = permissions.HasKMUserAccess()

    expected = request_method in SAFE_METHODS

    assert perm_instance.has_permission(request, view) == expected


@pytest.mark.parametrize("request_method", ALL_METHODS)
def test_shared_unaccepted(
        api_rf,
        km_user_accessor_factory,
        km_user_factory,
        request_method,
        user_factory):
    """
    Accessors that have not been accepted should not grant access.
    """
    km_user = km_user_factory()
    user = user_factory()

    km_user_accessor_factory(
        is_accepted=False,
        km_user=km_user,
        user_with_access=user)

    api_rf.user = user
    request = api_rf.generic(request_method, '/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': km_user.pk}

    perm_instance = permissions.HasKMUserAccess()

    with pytest.raises(Http404):
        perm_instance.has_permission(request, view)
