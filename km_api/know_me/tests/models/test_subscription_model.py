

def test_string_conversion(subscription_factory):
    """
    Converting a subscription to a string should return a user readable
    string containing the name of the user the subscription is
    associated with.
    """
    subscription = subscription_factory()
    expected = 'Know Me subscription for {user}'.format(
        user=subscription.user.get_full_name(),
    )

    assert str(subscription) == expected
