import datetime
from unittest import mock

import pytest
from django.utils import timezone
from rest_framework.exceptions import ValidationError as DRFValidationError

from know_me import subscriptions
from know_me.serializers import subscription_serializers
from know_me.subscriptions import AppleReceipt
from test_utils import serialized_time


def test_serialize(apple_subscription_factory):
    """
    Test serializing an Apple subscription.
    """
    subscription = apple_subscription_factory()
    serializer = subscription_serializers.AppleSubscriptionSerializer(
        subscription
    )

    expected = {
        "id": subscription.id,
        "time_created": serialized_time(subscription.time_created),
        "time_updated": serialized_time(subscription.time_updated),
        "expiration_time": serialized_time(subscription.expiration_time),
        "receipt_data": subscription.receipt_data,
    }

    assert serializer.data == expected


def test_validate_duplicate_receipt(apple_subscription_factory):
    """
    If the receipt data provided is already in use, validation should
    raise an error.
    """
    receipt_data = "some-receipt-data"
    apple_subscription_factory(receipt_data=receipt_data)

    serializer = subscription_serializers.AppleSubscriptionSerializer(
        data={"receipt_data": receipt_data}
    )

    assert not serializer.is_valid()
    assert serializer.errors == {
        "receipt_data": ["This receipt has already been used."]
    }


@mock.patch(
    "know_me.serializers.subscription_serializers.subscriptions.validate_apple_receipt",  # noqa
    autospec=True,
)
def test_validate_receipt_data(mock_validate_apple, db):
    """
    The serializer should validate the provided receipt data using the
    Apple subscription verification method.
    """
    expires = timezone.now().replace(microsecond=0) + datetime.timedelta(
        days=30
    )

    receipt_response = {
        "expires_date_ms": str(int(expires.timestamp() * 1000)),
        "product_id": "foo",
    }
    mock_validate_apple.return_value = AppleReceipt(receipt_response)

    receipt_data = "test-data"
    serializer = subscription_serializers.AppleSubscriptionSerializer(
        data={"receipt_data": receipt_data}
    )

    assert serializer.is_valid()

    assert mock_validate_apple.call_count == 1
    assert mock_validate_apple.call_args[0] == (receipt_data,)
    assert serializer.validated_data["expiration_time"] == expires


def test_validate_receipt_data_invalid(db):
    """
    If the receipt validation returns an error, it should be caught and
    re-raised as a ``ValidationError``.
    """
    ex_code = "invalid_receipt"
    ex_msg = "Invalid foo bar."
    receipt_data = "invalid-data"

    serializer = subscription_serializers.AppleSubscriptionSerializer(
        data={"receipt_data": receipt_data}
    )

    with mock.patch(
        "know_me.serializers.subscription_serializers.subscriptions.validate_apple_receipt",  # noqa
        autospec=True,
        side_effect=subscriptions.ReceiptException(ex_msg, ex_code),
    ):
        with pytest.raises(DRFValidationError) as error:
            serializer.is_valid(raise_exception=True)

    assert error.value.detail["receipt_data"][0] == ex_msg
    assert error.value.detail["receipt_data"][0].code == ex_code
