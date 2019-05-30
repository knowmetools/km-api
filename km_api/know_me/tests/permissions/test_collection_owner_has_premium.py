from unittest import mock

import pytest
from django.http import Http404

from know_me.permissions import CollectionOwnerHasPremium


def test_has_permission_active_subscription(
    api_rf, enable_premium_requirement, user_factory
):
    """
    If the user that the view states is the collection's owner has an
    active premium subscription, the check should return ``True``.
    """
    user = user_factory(has_premium=True)
    request = api_rf.get("/")

    view = mock.Mock(name="Mock View")
    view.get_subscription_owner.return_value = user

    perm = CollectionOwnerHasPremium()

    assert perm.has_permission(request, view)
    assert view.get_subscription_owner.call_args[0] == (request,)


def test_has_permission_inactive_subscription(
    api_rf, enable_premium_requirement, user_factory
):
    """
    If the user that the view states is the collection's owner has an
    inactive premium subscription, the check should return ``False``.
    """
    user = user_factory(has_premium=False)
    request = api_rf.get("/")

    view = mock.Mock(name="Mock View")
    view.get_subscription_owner.return_value = user

    perm = CollectionOwnerHasPremium()

    with pytest.raises(Http404):
        perm.has_permission(request, view)

    assert view.get_subscription_owner.call_args[0] == (request,)


def test_has_permission_inactive_subscription_feature_disabled(
    api_rf, user_factory
):
    """
    If the user that the view states is the collection's owner has an
    inactive premium subscription but the premium feature is not
    enabled, then the check should return ``True``.
    """
    request = api_rf.get("/")
    view = mock.Mock(name="Mock View")

    perm = CollectionOwnerHasPremium()

    assert perm.has_permission(request, view)
