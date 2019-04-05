from unittest import mock

import pytest
from django.http import Http404

from know_me.permissions import OwnerHasPremium


def test_has_object_permission_active_subscription(api_rf, user_factory):
    """
    If the user that the view states is the object's owner has an active
    premium subscription, the check should return ``True``.
    """
    user = user_factory(has_premium=True)
    request = api_rf.get("/")

    view = mock.Mock(name="Mock View")
    view.get_subscription_owner.return_value = user

    perm = OwnerHasPremium()
    obj = mock.Mock(name="Mock Object")

    assert perm.has_object_permission(request, view, obj)
    assert view.get_subscription_owner.call_args[0] == (request, obj)


def test_has_object_permission_inactive_subscription(api_rf, user_factory):
    """
    If the user that the view states is the object's owner has an
    inactive premium subscription, the check should return ``False``.
    """
    user = user_factory(has_premium=False)
    request = api_rf.get("/")

    view = mock.Mock(name="Mock View")
    view.get_subscription_owner.return_value = user

    perm = OwnerHasPremium()
    obj = mock.Mock(name="Mock Object")

    with pytest.raises(Http404):
        perm.has_object_permission(request, view, obj)

    assert view.get_subscription_owner.call_args[0] == (request, obj)
