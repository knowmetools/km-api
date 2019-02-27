from unittest import mock

import pytest
from rest_framework.exceptions import ValidationError as DRFValidationError

from know_me import subscriptions
from know_me.serializers import subscription_serializers


@mock.patch(
    "know_me.serializers.subscription_serializers.subscriptions.validate_apple_receipt",  # noqa
    autospec=True,
)
def test_create(_, subscription_factory):
    """
    Test deserializing data to create an Apple subscription.
    """
    base_subscription = subscription_factory()
    data = {"receipt_data": "receipt data"}

    serializer = subscription_serializers.AppleSubscriptionSerializer(
        data=data
    )
    assert serializer.is_valid()

    subscription = serializer.save(subscription=base_subscription)

    assert subscription.receipt_data == data["receipt_data"]


def test_serialize(apple_subscription_factory, serialized_time):
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
        "receipt_data": subscription.receipt_data,
    }

    assert serializer.data == expected


@mock.patch(
    "know_me.serializers.subscription_serializers.subscriptions.validate_apple_receipt",  # noqa
    autospec=True,
)
def test_validate_receipt_data(mock_validate_apple):
    """
    The serializer should validate the provided receipt data using the
    Apple subscription verification method.
    """
    receipt_data = "test-data"
    serializer = subscription_serializers.AppleSubscriptionSerializer(
        data={"receipt_data": receipt_data}
    )

    serializer.validate_receipt_data(receipt_data)

    assert mock_validate_apple.call_count == 1
    assert mock_validate_apple.call_args[0] == (receipt_data,)


def test_validate_receipt_data_invalid():
    """
    If the receipt validation returns an error, it should be caught and
    re-raised as a ``ValidationError``.
    """
    ex_code = "invalid_receipt"
    ex_msg = "Invalid foo bar."
    receipt_data = "invalid-data"

    serializer = subscription_serializers.AppleSubscriptionSerializer()

    with mock.patch(
        "know_me.serializers.subscription_serializers.subscriptions.validate_apple_receipt",  # noqa
        autospec=True,
        side_effect=subscriptions.ReceiptException(ex_msg, ex_code),
    ):
        with pytest.raises(DRFValidationError) as error:
            serializer.validate_receipt_data(receipt_data)

    assert error.value.detail[0] == ex_msg
    assert error.value.detail[0].code == ex_code
