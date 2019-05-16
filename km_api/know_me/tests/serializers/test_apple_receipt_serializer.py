import datetime
from unittest import mock

import pytest
from django.utils import timezone
from rest_framework.serializers import ValidationError as DRFValidationError

from know_me import models
from know_me.serializers import subscription_serializers
from know_me.subscriptions import ReceiptException
from test_utils import serialized_time


@pytest.fixture(autouse=True)
def mock_apple_receipt_objects():
    """
    Fixture to mock the queryset returned when working with Apple
    Receipts using the ORM.

    By default it pretends that no Apple receipts exist.
    """
    mock_queryset = mock.Mock(spec=models.AppleReceipt.objects)
    mock_queryset.exclude.return_value = mock_queryset
    mock_queryset.exists.return_value = False
    mock_queryset.filter.return_value = mock_queryset

    with mock.patch("know_me.models.AppleReceipt.objects", new=mock_queryset):
        yield mock_queryset


def test_save_expired():
    """
    Saving the serializer should save the instance associated with the
    serializer and deactivate the subscription passed in if the
    receipt's expiration time has passed.
    """
    now = timezone.now()
    expires = now - datetime.timedelta(days=1)

    with mock.patch(
        "know_me.serializers.subscription_serializers.timezone.now",
        autospec=True,
        return_value=now,
    ):
        serializer = subscription_serializers.AppleReceiptSerializer()
        serializer.instance = mock.Mock(name="Mock Apple Receipt")
        serializer.instance.expiration_time = expires
        subscription = mock.Mock(name="Mock Subscription")
        subscription.is_active = True

        serializer.save(subscription=subscription)

    assert not subscription.is_active
    assert subscription.save.call_count == 1
    assert serializer.instance.subscription == subscription
    assert serializer.instance.save.call_count == 1


def test_save_not_expired():
    """
    Saving the serializer should save the instance associated with the
    serializer and activate the subscription passed in if the receipt's
    expiration time has not yet passed.
    """
    now = timezone.now()
    expires = now + datetime.timedelta(days=1)

    with mock.patch(
        "know_me.serializers.subscription_serializers.timezone.now",
        autospec=True,
        return_value=now,
    ):
        serializer = subscription_serializers.AppleReceiptSerializer()
        serializer.instance = mock.Mock(name="Mock Apple Receipt")
        serializer.instance.expiration_time = expires
        subscription = mock.Mock(name="Mock Subscription")
        subscription.is_active = False

        serializer.save(subscription=subscription)

    assert subscription.is_active
    assert subscription.save.call_count == 1
    assert serializer.instance.subscription == subscription
    assert serializer.instance.save.call_count == 1


def test_serialize():
    """
    Test serializing an Apple subscription.
    """
    receipt = models.AppleReceipt(
        expiration_time=timezone.now(),
        receipt_data="foo",
        time_created=timezone.now(),
        time_updated=timezone.now(),
    )
    receipt.clean()
    serializer = subscription_serializers.AppleReceiptSerializer(receipt)

    expected = {
        "id": str(receipt.pk),
        "time_created": serialized_time(receipt.time_created),
        "time_updated": serialized_time(receipt.time_updated),
        "expiration_time": serialized_time(receipt.expiration_time),
        "receipt_data": receipt.receipt_data,
    }

    assert serializer.data == expected


@mock.patch("know_me.models.AppleReceipt.update_info", autospec=True)
def test_validate(mock_update_info):
    """
    Validating the serializer should attempt to update the info of an
    ``AppleReceipt`` instance and then persist that instance within the
    serializer so it can be saved.
    """
    receipt_data = "foo"
    serializer = subscription_serializers.AppleReceiptSerializer()

    serializer.validate({"receipt_data": receipt_data})

    assert serializer.instance.receipt_data == receipt_data
    assert mock_update_info.call_args[0] == (serializer.instance,)


@mock.patch("know_me.models.AppleReceipt.update_info", autospec=True)
def test_validate_update_info_fail(mock_update_info):
    """
    If updating the information of an Apple receipt fails, the emitted
    error should be echoed as a validation error.
    """
    exception = ReceiptException("foo", "bar")
    mock_update_info.side_effect = exception

    serializer = subscription_serializers.AppleReceiptSerializer()

    with pytest.raises(DRFValidationError) as exc_info:
        serializer.validate({"receipt_data": "baz"})

    assert exc_info.value.detail["receipt_data"] == exception.msg
    assert exc_info.value.detail["receipt_data"].code == exception.code


@mock.patch("know_me.models.AppleReceipt.update_info", autospec=True)
def test_validate_update_instance(mock_update_info):
    """
    If the serializer is already associated with an existing receipt
    instance, the validation process should use the existing instance
    instead of creating a new one.
    """
    receipt = models.AppleReceipt(receipt_data="foo")
    receipt_data = "bar"
    serializer = subscription_serializers.AppleReceiptSerializer(receipt)

    serializer.validate({"receipt_data": receipt_data})

    assert serializer.instance == receipt
    assert serializer.instance.receipt_data == receipt_data
    assert mock_update_info.call_args[0] == (receipt,)


@mock.patch("know_me.models.AppleReceipt.update_info", autospec=True)
def test_validate_non_unique(mock_update_info, mock_apple_receipt_objects):
    """
    If there is an existing receipt with the same original transaction
    ID as whatever the provided receipt data resolves to, a validation
    error should be thrown.
    """
    transaction_id = 1234

    def mock_update_func(receipt):
        receipt.transaction_id = transaction_id

    mock_update_info.side_effect = mock_update_func
    mock_apple_receipt_objects.exists.return_value = True

    serializer = subscription_serializers.AppleReceiptSerializer()

    with pytest.raises(DRFValidationError):
        serializer.validate({"receipt_data": "foo"})

    assert mock_apple_receipt_objects.exclude.call_args[1] == {
        "pk": serializer.instance.pk
    }
    assert mock_apple_receipt_objects.filter.call_args[1] == {
        "transaction_id": transaction_id
    }
    assert mock_apple_receipt_objects.exists.call_count == 1
