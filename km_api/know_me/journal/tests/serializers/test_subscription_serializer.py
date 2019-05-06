from know_me import models
from know_me.serializers import subscription_serializers


def test_serialize_inactive():
    """
    If an inactive subscription is serialized, ``is_active`` should be
    ``False`` and all other fields should be ``None``.
    """
    subscription = models.Subscription(is_active=False)
    serializer = subscription_serializers.SubscriptionSerializer(subscription)

    assert serializer.data == {
        "apple_receipt": None,
        "is_active": False,
        "is_legacy_subscription": False,
    }


def test_serialize_apple_receipt(apple_receipt_factory):
    """
    If a subscription backed by an Apple receipt is serialized, it
    should return information about the Apple receipt.
    """
    receipt = apple_receipt_factory(subscription__is_active=True)
    serializer = subscription_serializers.SubscriptionSerializer(
        receipt.subscription
    )

    # Child serializers
    receipt_serializer = subscription_serializers.AppleReceiptInfoSerializer(
        receipt
    )

    assert serializer.data == {
        "apple_receipt": receipt_serializer.data,
        "is_active": True,
        "is_legacy_subscription": False,
    }


def test_serialize_legacy(subscription_factory):
    """
    If a subscription is marked as a legacy subscription, it should
    include a flag indicating that.
    """
    subscription = subscription_factory(is_legacy_subscription=True)
    serializer = subscription_serializers.SubscriptionSerializer(subscription)

    assert serializer.data == {
        "apple_receipt": None,
        "is_active": subscription.is_active,
        "is_legacy_subscription": True,
    }
