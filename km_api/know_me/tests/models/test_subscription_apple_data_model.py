

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
