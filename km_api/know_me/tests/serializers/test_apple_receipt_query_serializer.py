from know_me.serializers import subscription_serializers


def test_serialize(apple_receipt_factory):
    """
    Serializing an Apple receipt in response to a query should return
    the receipt's data hash and the owner's primary email address.
    """
    receipt = apple_receipt_factory()
    serializer = subscription_serializers.AppleReceiptQuerySerializer(receipt)

    assert serializer.data == {
        "email": receipt.subscription.user.primary_email.email,
        "receipt_data_hash": receipt.receipt_data_hash,
    }
