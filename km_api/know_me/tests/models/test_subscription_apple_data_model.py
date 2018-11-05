

def test_has_object_read_permission_owner(api_rf, apple_subscription_factory):
    """
    The owner of the subscription should have read access to it.
    """
    subscription = apple_subscription_factory()
    api_rf.user = subscription.subscription.user
    request = api_rf.get('/')

    assert subscription.has_object_read_permission(request)


def test_has_object_read_permission_other(
        api_rf,
        apple_subscription_factory,
        user_factory):
    """
    If the requesting user does not own the subscription, they should
    not be granted read access.
    """
    subscription = apple_subscription_factory()
    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not subscription.has_object_read_permission(request)


def test_has_object_write_permission_owner(api_rf, apple_subscription_factory):
    """
    The owner of the subscription should have write access to it.
    """
    subscription = apple_subscription_factory()
    api_rf.user = subscription.subscription.user
    request = api_rf.get('/')

    assert subscription.has_object_write_permission(request)


def test_has_object_write_permission_other(
        api_rf,
        apple_subscription_factory,
        user_factory):
    """
    If the requesting user does not own the subscription, they should
    not be granted write access.
    """
    subscription = apple_subscription_factory()
    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not subscription.has_object_write_permission(request)


def test_string_conversion(apple_subscription_factory):
    """
    Converting an instance to a string should return a user readable
    string containing information about the parent subscription.
    """
    data = apple_subscription_factory()
    expected = 'Apple subscription data for the {subscription}'.format(
        subscription=data.subscription,
    )

    assert str(data) == expected
