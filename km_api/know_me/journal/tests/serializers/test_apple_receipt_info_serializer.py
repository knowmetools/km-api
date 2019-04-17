from know_me.serializers import subscription_serializers
from test_utils import serialized_time


def test_serialize(apple_subscription_factory):
    """
    Serializing an Apple receipt should return an overview of the
    information contained in the receipt.
    """
    apple_receipt = apple_subscription_factory()
    serializer = subscription_serializers.AppleReceiptInfoSerializer(
        apple_receipt
    )

    assert serializer.data == {
        "expiration_time": serialized_time(apple_receipt.expiration_time),
        "receipt_data_hash": apple_receipt.receipt_data_hash,
    }
