from know_me.serializers import subscription_serializers


def test_serialize_inactive(subscription_factory):
    """
    If an inactive subscription is serialized, ``is_active`` should be
    ``False`` and all other fields should be ``None``.
    """
    subscription = subscription_factory(is_active=False)
    serializer = subscription_serializers.SubscriptionSerializer(subscription)

    assert serializer.data == {"apple_receipt": None, "is_active": False}


def test_serialize_apple_receipt(apple_subscription_factory):
    """
    If a subscription backed by an Apple receipt is serialized, it
    should return information about the Apple receipt.
    """
    apple_receipt = apple_subscription_factory(subscription__is_active=True)
    serializer = subscription_serializers.SubscriptionSerializer(
        apple_receipt.subscription
    )

    # Child serializers
    apple_receipt_serializer = subscription_serializers.AppleReceiptInfoSerializer(  # noqa
        apple_receipt
    )

    assert serializer.data == {
        "apple_receipt": apple_receipt_serializer.data,
        "is_active": True,
    }
