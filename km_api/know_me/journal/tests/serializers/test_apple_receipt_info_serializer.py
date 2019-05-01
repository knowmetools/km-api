from django.utils import timezone

from know_me import models
from know_me.serializers import subscription_serializers
from test_utils import serialized_time


def test_serialize():
    """
    Serializing an Apple receipt should return an overview of the
    information contained in the receipt.
    """
    receipt = models.AppleReceipt(
        expiration_time=timezone.now(),
        receipt_data_hash=models.AppleReceipt.hash_data("foo"),
    )
    serializer = subscription_serializers.AppleReceiptInfoSerializer(receipt)

    assert serializer.data == {
        "expiration_time": serialized_time(receipt.expiration_time),
        "receipt_data_hash": receipt.receipt_data_hash,
    }
