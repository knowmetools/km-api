import datetime
from unittest import mock

import pytest
from django.utils import timezone
from rest_framework.exceptions import ValidationError as DRFValidationError

from know_me import subscriptions
from know_me.serializers import subscription_serializers
from know_me.subscriptions import AppleTransaction
from test_utils import serialized_time, receipt_data_hash


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
        "latest_receipt_data": subscription.latest_receipt_data,
        "latest_receipt_data_hash": subscription.latest_receipt_data_hash,
        "receipt_data": subscription.receipt_data,
        "receipt_data_hash": receipt_data_hash(subscription.receipt_data),
    }

    assert serializer.data == expected


@mock.patch(
    "know_me.serializers.subscription_serializers.subscriptions.validate_apple_receipt",  # noqa
    autospec=True,
)
def test_validate_object(mock_validate_apple, db):
    """
    The serializer should validate the provided receipt data using the
    Apple subscription verification method.
    """
    expires = timezone.now().replace(microsecond=0) + datetime.timedelta(
        days=30
    )

    receipt_data = "test-data"
    receipt_response = {
        "expires_date_ms": str(int(expires.timestamp() * 1000)),
        "product_id": "foo",
    }
    mock_validate_apple.return_value = AppleTransaction(
        receipt_response, receipt_data
    )

    serializer = subscription_serializers.AppleSubscriptionSerializer(
        data={"receipt_data": receipt_data}
    )

    assert serializer.is_valid()

    assert mock_validate_apple.call_count == 1
    assert mock_validate_apple.call_args[0] == (receipt_data,)
    assert serializer.validated_data["expiration_time"] == expires
    assert serializer.validated_data["latest_receipt_data"] == receipt_data
    assert serializer.validated_data[
        "latest_receipt_data_hash"
    ] == receipt_data_hash(receipt_data)
    assert serializer.validated_data["receipt_data_hash"] == receipt_data_hash(
        receipt_data
    )


@mock.patch(
    "know_me.serializers.subscription_serializers.subscriptions.validate_apple_receipt",  # noqa
    autospec=True,
)
def test_validate_object_duplicate_matches_latest_receipt_data(
    mock_validate_apple, apple_subscription_factory
):
    """
    If the latest receipt data returned when the receipt is validated
    matches an existing Apple receipt's latest data, a validation error
    should be raised.
    """
    existing_receipt = apple_subscription_factory(
        latest_receipt_data="foo", receipt_data="bar"
    )
    mock_validate_apple.return_value = AppleTransaction(
        {}, existing_receipt.latest_receipt_data
    )

    serializer = subscription_serializers.AppleSubscriptionSerializer(
        data={"receipt_data": "baz"}
    )

    assert not serializer.is_valid()
    assert serializer.errors == {
        "receipt_data": ["This receipt has already been used."]
    }


@mock.patch(
    "know_me.serializers.subscription_serializers.subscriptions.validate_apple_receipt",  # noqa
    autospec=True,
)
def test_validate_object_duplicate_matches_original_receipt_data(
    mock_validate_apple, apple_subscription_factory
):
    """
    If the latest receipt data returned when the receipt is validated
    matches an existing Apple receipt's original data, a validation
    error should be raised.
    """
    existing_receipt = apple_subscription_factory(
        latest_receipt_data="foo", receipt_data="bar"
    )
    mock_validate_apple.return_value = AppleTransaction(
        {}, existing_receipt.receipt_data
    )

    serializer = subscription_serializers.AppleSubscriptionSerializer(
        data={"receipt_data": "baz"}
    )

    assert not serializer.is_valid()
    assert serializer.errors == {
        "receipt_data": ["This receipt has already been used."]
    }


def test_validate_object_receipt_data_invalid(db):
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


def test_validate_receipt_data_duplicate_latest_receipt(
    apple_subscription_factory
):
    """
    If the provided receipt data matches the latest receipt data of an
    existing receipt, validation should raise an error.
    """
    receipt_data = "foo"
    apple_subscription_factory(
        latest_receipt_data=receipt_data, receipt_data="bar"
    )

    serializer = subscription_serializers.AppleSubscriptionSerializer()

    with pytest.raises(DRFValidationError) as error:
        serializer.validate_receipt_data(receipt_data)

    assert error.value.detail[0] == "This receipt has already been used."


def test_validate_receipt_data_duplicate_original_receipt(
    apple_subscription_factory
):
    """
    If the receipt data provided matches the original receipt data of a
    receipt already in use, validation should raise an error.
    """
    receipt_data = "some-receipt-data"
    apple_subscription_factory(receipt_data=receipt_data)

    serializer = subscription_serializers.AppleSubscriptionSerializer()

    with pytest.raises(DRFValidationError) as error:
        serializer.validate_receipt_data(receipt_data)

    assert error.value.detail[0] == "This receipt has already been used."
