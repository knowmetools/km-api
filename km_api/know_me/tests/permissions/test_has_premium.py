from unittest import mock

from know_me.permissions import HasPremium


def test_has_permission_active_subscription(
    api_rf, enable_premium_requirement, user_factory
):
    """
    If the requesting user has an active premium subscription, the
    permission should return ``True``.
    """
    user = user_factory(has_premium=True)
    api_rf.user = user

    request = api_rf.get("/")
    view = mock.Mock(name="Mock View")

    perm = HasPremium()

    assert perm.has_permission(request, view)


def test_has_permission_anonymous(api_rf, enable_premium_requirement):
    """
    If the requesting user is anonymous, permission should be denied.
    """
    request = api_rf.get("/")
    view = mock.Mock(name="Mock View")

    perm = HasPremium()

    assert not perm.has_permission(request, view)


def test_has_permission_anonymous_no_premium_requirement(api_rf):
    """
    If the premium requirement is disabled, anonymous users should pass
    the check.
    """
    request = api_rf.get("/")
    view = mock.Mock(name="Mock View")

    perm = HasPremium()

    assert perm.has_permission(request, view)


def test_has_permission_inactive_subscription(
    api_rf, enable_premium_requirement, user_factory, subscription_factory
):
    """
    If the requesting user has an inactive subscription, permission
    should be denied.
    """
    user = user_factory()
    subscription_factory(is_active=False, user=user)
    api_rf.user = user

    request = api_rf.get("/")
    view = mock.Mock(name="Mock View")

    perm = HasPremium()

    assert not perm.has_permission(request, view)


def test_has_permission_no_subscription(
    api_rf, enable_premium_requirement, user_factory
):
    """
    If there is no subscription data associated with the requesting user
    then permission should be denied.
    """
    user = user_factory()
    api_rf.user = user

    request = api_rf.get("/")
    view = mock.Mock(name="Mock View")

    perm = HasPremium()

    assert not perm.has_permission(request, view)


def test_has_permission_no_subscription_feature_disabled(api_rf):
    """
    If the
    Args:
        api_rf:

    Returns:

    """
