import enum
import logging

import requests
from django.conf import settings


logger = logging.getLogger(__name__)


class ReceiptCodes(enum.IntEnum):
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
    TEST_RECEIPT = 21007  # Test receipt sent to production env
    PRODUCTION_RECEIPT = 21008  # Production receipt sent to test env
    COULD_NOT_AUTHORIZE = 21010


def get_receipt_info(receipt_data):
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
