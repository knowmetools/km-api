import datetime
import enum
import logging

import requests
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext

logger = logging.getLogger(__name__)


class AppleReceiptCodes(enum.IntEnum):
    """
    Enum containing the possible status codes that can be returned from
    Apple's receipt validation service.

    Codes taken from:
    https://developer.apple.com/library/archive/releasenotes/General/ValidateAppStoreReceipt/Chapters/ValidateRemotely.html#//apple_ref/doc/uid/TP40010573-CH104-SW5
    """

    VALID = 0
    MALFORMED_RECEIPT_DATA = 21002
    COULD_NOT_AUTHENTICATE = 21003
    UNAVAILABLE = 21005
    COULD_NOT_AUTHORIZE = 21010


APPLE_ERROR_MSGS = {
    AppleReceiptCodes.COULD_NOT_AUTHENTICATE: _(
        "The provided receipt data is not valid."
    ),
    AppleReceiptCodes.COULD_NOT_AUTHORIZE: _(
        "The provided receipt data is not valid."
    ),
    AppleReceiptCodes.MALFORMED_RECEIPT_DATA: _(
        "The provided receipt data is malformed."
    ),
    AppleReceiptCodes.UNAVAILABLE: _(
        "Apple's servers are unavailable to verify your receipt. Please try "
        "again later."
    ),
    21007: _(
        "This receipt was created in the test environment and may not be "
        "verified against the production environment."
    ),
    21008: _(
        "This receipt was created in the production environment and may not "
        "be verified against the test environment."
    ),
}


class ReceiptException(Exception):
    """
    Base exception class for invalid receipts.
    """

    def __init__(self, msg, code="invalid_receipt"):
        """
        Create a new receipt exception.

        Args:
            msg:
                The message describing why the receipt is invalid.
            code:
                A code categorizing the exception.
        """
        self.msg = msg
        self.code = code


class InvalidReceiptTypeException(ReceiptException):
    """
    Exception indicating the wrong type of receipt was provided.
    """

    pass


class ReceiptServerException(ReceiptException):
    """
    Exception indicating there was an error while communicating with the
    server used to verify a receipt.
    """

    pass


class AppleTransaction:
    """
    A container for a single transaction from a renewable subscription
    through the Apple store.
    """

    def __init__(self, transaction: dict, latest_receipt_data: str):
        """
        Create a new instance representing a single transaction.

        Args:
            transaction:
                A dictionary containing information about a single
                transaction from a renewable subscription.
            latest_receipt_data:
                The base64 encoded receipt data from the most recent
                receipt that can be used to identify the transaction.
        """
        self.raw_info = transaction
        self.latest_receipt_data = latest_receipt_data

    def __eq__(self, other):
        """
        Determine if the transaction is equivalent to another object.

        Two transaction container instances are equal iff they map to
        the same raw data.

        Args:
            other:
                The object to test this instance for equality to.

        Returns:
            A boolean indicating if this instance is equal to the other
            object.
        """
        if isinstance(other, AppleTransaction):
            return (
                self.raw_info == other.raw_info
                and self.latest_receipt_data == other.latest_receipt_data
            )

        return super().__eq__(other)

    @property
    def expires_date(self) -> datetime.datetime:
        """
        Returns:
            A :class:`datetime.datetime` instance representing the time
            that the transaction expires.
        """
        return datetime.datetime.fromtimestamp(
            int(self.raw_info["expires_date_ms"]) // 1000,
            datetime.timezone.utc,
        )

    @property
    def original_transaction_id(self):
        """
        Returns:
            The ID of the original transaction that led to the
            transaction represented by the instance.
        """
        return int(self.raw_info["original_transaction_id"])

    @property
    def product_id(self):
        """
        Returns:
            The ID of the product that the transaction is for.
        """
        return self.raw_info["product_id"]


def get_apple_receipt_info(receipt_data):
    """
    Get information about an Apple receipt by sending its base64 encoded
    data.

    Args:
        receipt_data:
            The base64 encoded receipt data that is sent to Apple to
            verify.

    Returns:
        The receipt data returned by Apple.
    """
    logger.debug(
        "Sending receipt data to apple for validation: %s", receipt_data
    )

    data = None
    retry = True
    while retry:
        response = requests.post(
            settings.APPLE_RECEIPT_VALIDATION_ENDPOINT,
            json={
                "password": settings.APPLE_SHARED_SECRET,
                "receipt-data": receipt_data,
            },
        )
        response.raise_for_status()
        data = response.json()

        # If Apple had some internal failure when returning the receipt,
        # the request should be retried.
        retry = data.get("is-retryable", False)

        if retry:
            logger.info("Retrying Apple receipt verification.")

    return data


def validate_apple_receipt(receipt_data):
    """
    A wrapper around :py:func:`get_apple_receipt_info` and
    :py:func:`validate_apple_receipt_response`. It takes the provided
    receipt data, gets a response from the Apple receipt validation
    server, passes that to the validation method, then returns the
    result.

    Args:
        receipt_data:
            The receipt data to validate.

    Returns:
        The output of the :py:func:`validate_apple_receipt_response`
        function.
    """
    receipt_info = get_apple_receipt_info(receipt_data)

    return validate_apple_receipt_response(receipt_info)


def validate_apple_receipt_response(receipt_response):
    """
    Validate an Apple receipt to ensure it is an auto-renewable
    subscription for a valid product.

    Args:
        receipt_response:
            The response data for the receipt received from the Apple
            receipt validation service.

    Returns:
        The information of the most recent transaction associated with
        the receipt.
    """
    status = receipt_response["status"]

    # Handle unavailability as a special case since it throws a
    # different exception type.
    if status == AppleReceiptCodes.UNAVAILABLE:
        logger.error("Apple receipt validation service unavailable.")

        raise ReceiptServerException(
            APPLE_ERROR_MSGS[AppleReceiptCodes.UNAVAILABLE]
        )

    # If the received status is present in the mapping of error messages
    # then raise an error.
    if status in APPLE_ERROR_MSGS:
        raise InvalidReceiptTypeException(APPLE_ERROR_MSGS[status])

    # Before we start processing receipt data, ensure that only a valid
    # receipt is allowed through.
    if status != AppleReceiptCodes.VALID:
        raise ValueError(
            f"Expected Apple receipt to have a valid status code. Got "
            f"{status} instead."
        )

    if "latest_receipt_info" not in receipt_response:
        raise InvalidReceiptTypeException(
            ugettext(
                "Expected a subscription receipt but received a consumable "
                "receipt instead."
            )
        )

    latest_receipts = receipt_response["latest_receipt_info"]
    if not latest_receipts:
        raise InvalidReceiptTypeException(
            ugettext("The provided receipt does not have any transactions.")
        )

    latest_transaction = latest_receipts[-1]
    product = latest_transaction.get("product_id")

    if product not in settings.APPLE_PRODUCT_CODES["KNOW_ME_PREMIUM"]:
        logger.info(
            "Received receipt that included a transaction for the unknown "
            'product "%s"',
            product,
        )

        raise InvalidReceiptTypeException(
            ugettext("Receipt contains transactions for an invalid product.")
        )

    return AppleTransaction(
        latest_transaction, receipt_response["latest_receipt"]
    )
