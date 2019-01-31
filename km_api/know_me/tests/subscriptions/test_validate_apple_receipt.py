import pytest

from know_me.subscriptions import (
    InvalidReceiptTypeException,
    validate_apple_receipt,
    ReceiptServerException,
)


class ReceiptCode:
    VALID = 0
    MALFORMED_RECEIPT_DATA = 21002
    UNAVAILABLE = 21005


def test_validate_apple_receipt_invalid_product_code(settings):
    """
    If any of the transactions in the receipt have an invalid product
    code, a validation error should be raised.
    """
    settings.APPLE_PRODUCT_CODES["KNOW_ME_PREMIUM"] = ["annual"]
    receipt_response = {
        "latest_receipt_info": [
            {"product_id": "annual"},
            {"product_id": "invalid"},
        ],
        "status": ReceiptCode.VALID,
    }

    with pytest.raises(InvalidReceiptTypeException):
        validate_apple_receipt(receipt_response)


def tests_validate_apple_receipt_malformed_data():
    """
    If Apple returns a response indicating that the provided data was
    invalid an exception should be raised.
    """
    receipt_response = {"status": ReceiptCode.MALFORMED_RECEIPT_DATA}

    with pytest.raises(InvalidReceiptTypeException):
        validate_apple_receipt(receipt_response)


def test_validate_apple_receipt_not_auto_renewable():
    """
    If the provided receipt data is not for an auto-renewable
    subscription an exception should be raised.
    """
    with pytest.raises(InvalidReceiptTypeException):
        # The lack of the 'latest_receipt_info' field indicates that
        # this receipt is not for an auto-renewable subscription.
        validate_apple_receipt({"status": ReceiptCode.VALID})


def test_validate_apple_receipt_unavailable():
    """
    If Apple returns a response code indicating the receipt validation
    service is unavailable, an error should be raised.
    """
    receipt_response = {"status": ReceiptCode.UNAVAILABLE}

    with pytest.raises(ReceiptServerException):
        validate_apple_receipt(receipt_response)


@pytest.mark.parametrize("product_code", ["annual", "monthly"])
def test_validate_apple_receipt_valid(product_code, settings):
    """
    If the provided receipt data is valid, nothing should happen.
    """
    settings.APPLE_PRODUCT_CODES["KNOW_ME_PREMIUM"] = ["annual", "monthly"]

    validate_apple_receipt(
        {
            "latest_receipt_info": [{"product_id": product_code}],
            "status": ReceiptCode.VALID,
        }
    )
