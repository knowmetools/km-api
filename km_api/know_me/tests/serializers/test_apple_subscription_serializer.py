from know_me.serializers import subscription_serializers


def test_create(subscription_factory):
    """
    Test deserializing data to create an Apple subscription.
    """
    base_subscription = subscription_factory()
    data = {
        'receipt_data': 'receipt data',
    }

    serializer = subscription_serializers.AppleSubscriptionSerializer(
        data=data,
    )
    assert serializer.is_valid()

    subscription = serializer.save(subscription=base_subscription)

    assert subscription.receipt_data == data['receipt_data']


def test_serialize(apple_subscription_factory, serialized_time):
    """
    Test serializing an Apple subscription.
    """
    subscription = apple_subscription_factory()
    serializer = subscription_serializers.AppleSubscriptionSerializer(
        subscription,
    )

    expected = {
        'id': subscription.id,
        'time_created': serialized_time(subscription.time_created),
        'time_updated': serialized_time(subscription.time_updated),
        'receipt_data': subscription.receipt_data,
    }

    assert serializer.data == expected
