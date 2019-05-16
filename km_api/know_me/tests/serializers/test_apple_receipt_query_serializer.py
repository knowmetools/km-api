from unittest import mock

import pytest
from rest_framework.exceptions import ValidationError as DRFValidationError

from know_me import models
from know_me.serializers import subscription_serializers
from know_me.subscriptions import ReceiptException, AppleTransaction


def test_save():
    """
    The save method of the serializer should be a no-op and thus
    callable from an empty serializer.
    """
    serializer = subscription_serializers.AppleReceiptQuerySerializer()
    serializer.save()


def test_validate_in_use(mock_apple_receipt_qs):
    """
    If there is an existing Apple receipt with the same original
    transaction ID as the submitted receipt, the validated data's
    ``is_used`` flag should be ``True`` and the ``email`` field should
    be populated.
    """
    email = "test@example.com"
    email_inst = mock.Mock()
    email_inst.email = email
    receipt = mock.Mock()
    type(receipt.subscription.user).primary_email = mock.PropertyMock(
        return_value=email_inst
    )

    mock_apple_receipt_qs.get.return_value = receipt

    serializer = subscription_serializers.AppleReceiptQuerySerializer()
    serializer._receipt_info = AppleTransaction(
        {"original_transaction_id": receipt.transaction_id}, "foo"
    )

    validated = serializer.validate({"receipt_data": "foo"})

    assert validated["email"] == email
    assert validated["is_used"]
    assert mock_apple_receipt_qs.get.call_args[1] == {
        "transaction_id": serializer._receipt_info.original_transaction_id
    }


def test_validate_not_used(mock_apple_receipt_qs):
    """
    If there is not an existing Apple receipt with the same original
    transaction ID as the submitted receipt, the validated data's
    ``is_used`` flag should be ``False`` and the ``email`` field should
    not be populated.
    """
    mock_apple_receipt_qs.get.side_effect = models.AppleReceipt.DoesNotExist

    serializer = subscription_serializers.AppleReceiptQuerySerializer()
    serializer._receipt_info = AppleTransaction(
        {"original_transaction_id": "abc"}, "foo"
    )

    validated = serializer.validate({"receipt_data": "foo"})

    assert validated["email"] is None
    assert not validated["is_used"]
    assert mock_apple_receipt_qs.get.call_args[1] == {
        "transaction_id": serializer._receipt_info.original_transaction_id
    }


@mock.patch(
    "know_me.serializers.subscription_serializers.subscriptions.validate_apple_receipt",  # noqa
    autospec=True,
)
def test_validate_receipt_data_invalid(mock_validate):
    """
    If the provided receipt data is invalid, a validation error should
    be raised with the information from the receipt validation error.
    """
    exception = ReceiptException("foo", "bar")
    mock_validate.side_effect = exception

    serializer = subscription_serializers.AppleReceiptQuerySerializer()

    with pytest.raises(DRFValidationError) as exc_info:
        serializer.validate_receipt_data("baz")

    assert exc_info.value.detail[0] == exception.msg
    assert exc_info.value.detail[0].code == exception.code


@mock.patch(
    "know_me.serializers.subscription_serializers.subscriptions.validate_apple_receipt",  # noqa
    autospec=True,
)
def test_validate_receipt_data_valid(mock_validate):
    """
    If the provided apple receipt is valid, validating it should persist
    the receipt's data within the serializer.
    """
    receipt_data = "foo"
    serializer = subscription_serializers.AppleReceiptQuerySerializer()

    result = serializer.validate_receipt_data(receipt_data)

    assert result == receipt_data
    assert mock_validate.call_args[0] == (receipt_data,)
    assert serializer._receipt_info == mock_validate.return_value
