import enum

import pytest

from know_me.subscriptions import (
    AppleReceiptCodes,
    AppleTransaction,
    InvalidReceiptTypeException,
    ReceiptServerException,
    validate_apple_receipt_response,
)


class ReceiptCode(enum.IntEnum):
    VALID = 0
    MALFORMED_RECEIPT_DATA = 21002
    COULD_NOT_BE_AUTHENTICATED = 21003
    UNAVAILABLE = 21005
    COULD_NOT_BE_AUTHORIZED = 21010


def test_validate_apple_receipt_could_not_authenticate():
    """
    If Apple returns a response indicating that the provided receipt
    data could not be authenticated, a validation error should be
    raised.
    """
    receipt_response = {"status": ReceiptCode.COULD_NOT_BE_AUTHENTICATED}

    with pytest.raises(InvalidReceiptTypeException):
        validate_apple_receipt_response(receipt_response)


def test_validate_apple_receipt_could_not_authorized():
    """
    If Apple returns a response indicating that the provided receipt
    data could not be authorized, a validation error should be raised.
    """
    receipt_response = {"status": ReceiptCode.COULD_NOT_BE_AUTHORIZED}

    with pytest.raises(InvalidReceiptTypeException):
        validate_apple_receipt_response(receipt_response)


def test_validate_apple_receipt_invalid_product_code(settings):
    """
    If the latest transaction has an invalid product code, a validation
    error should be raised.
    """
    settings.APPLE_PRODUCT_CODES["KNOW_ME_PREMIUM"] = ["annual"]
    receipt_response = {
        "latest_receipt_info": [{"product_id": "invalid"}],
        "status": ReceiptCode.VALID,
    }

    with pytest.raises(InvalidReceiptTypeException):
        validate_apple_receipt_response(receipt_response)


def tests_validate_apple_receipt_malformed_data():
    """
    If Apple returns a response indicating that the provided data was
    invalid an exception should be raised.
    """
    receipt_response = {"status": ReceiptCode.MALFORMED_RECEIPT_DATA}

    with pytest.raises(InvalidReceiptTypeException):
        validate_apple_receipt_response(receipt_response)


def test_validate_apple_receipt_no_transactions():
    """
    If the provided response does not include any transactions, an
    exception should be raised.
    """
    with pytest.raises(InvalidReceiptTypeException):
        validate_apple_receipt_response(
            {"status": ReceiptCode.VALID, "latest_receipt_info": []}
        )


def test_validate_apple_receipt_not_auto_renewable():
    """
    If the provided receipt data is not for an auto-renewable
    subscription an exception should be raised.
    """
    with pytest.raises(InvalidReceiptTypeException):
        # The lack of the 'latest_receipt_info' field indicates that
        # this receipt is not for an auto-renewable subscription.
        validate_apple_receipt_response({"status": ReceiptCode.VALID})


def test_validate_apple_receipt_unavailable():
    """
    If Apple returns a response code indicating the receipt validation
    service is unavailable, an error should be raised.
    """
    receipt_response = {"status": ReceiptCode.UNAVAILABLE}

    with pytest.raises(ReceiptServerException):
        validate_apple_receipt_response(receipt_response)


def test_validate_apple_receipt_unknown_status():
    """
    If we get an unknown status code, an exception should be thrown.
    """
    unknown_status = 123

    # Quick sanity check to ensure that our code isn't one that is
    # actually used.
    assert unknown_status not in AppleReceiptCodes

    with pytest.raises(ValueError):
        validate_apple_receipt_response({"status": unknown_status})


@pytest.mark.parametrize("product_code", ["annual", "monthly"])
def test_validate_apple_receipt_valid(product_code, settings):
    """
    If the provided receipt data is valid, the most recent transaction
    should be returned.
    """
    settings.APPLE_PRODUCT_CODES["KNOW_ME_PREMIUM"] = ["annual", "monthly"]
    latest_receipt_data = "receipt-data"
    transaction_info = {
        "expires_date_ms": 0,
        "original_transaction_id": 123,
        "product_id": product_code,
    }

    result = validate_apple_receipt_response(
        {
            "latest_receipt": latest_receipt_data,
            "latest_receipt_info": [{"product_id": "foo"}, transaction_info],
            "status": ReceiptCode.VALID,
        }
    )

    assert result == AppleTransaction(transaction_info, latest_receipt_data)
