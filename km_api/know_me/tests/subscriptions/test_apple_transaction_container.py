import datetime

import pytest
from django.utils import timezone

from know_me import subscriptions


EXPIRES_DATE_MS = int(timezone.now().timestamp()) * 1000
PRODUCT_ID = "com.knowmetools.knowme.test"
TRANSACTION_ID = "1234"


@pytest.fixture
def transaction_info():
    """
    Returns:
        A dictionary containing valid transaction information.
    """
    return {
        "expires_date_ms": str(EXPIRES_DATE_MS),
        "original_transaction_id": TRANSACTION_ID,
        "product_id": PRODUCT_ID,
    }


def test_eq_identity(transaction_info):
    """
    An instance of the container should be equal to itself.
    """
    transaction = subscriptions.AppleTransaction(transaction_info, "foo")

    assert transaction == transaction


def test_eq_other_object(transaction_info):
    """
    A transaction instance should not be equivalent to an instance of
    another class.
    """
    transaction = subscriptions.AppleTransaction(transaction_info, "foo")

    assert transaction != 3


def test_eq_same_data(transaction_info):
    """
    If two transaction containers have the same data, they should be
    equal.
    """
    receipt_data = "foo"
    t1 = subscriptions.AppleTransaction(transaction_info, receipt_data)
    t2 = subscriptions.AppleTransaction(transaction_info, receipt_data)

    assert t1 == t2


def test_expires_date(transaction_info):
    """
    The expires date should return a datetime instance representing the
    same date as the ``expires_date_ms`` property from the raw
    transaction info.
    """
    transaction = subscriptions.AppleTransaction(transaction_info, "foo")
    expected = datetime.datetime.fromtimestamp(
        EXPIRES_DATE_MS // 1000, datetime.timezone.utc
    )

    assert transaction.expires_date == expected


def test_init_valid_data(transaction_info):
    """
    Passing valid transaction data to the container should store the
    data and parse some data out.
    """
    latest_receipt_data = "foo"

    transaction = subscriptions.AppleTransaction(
        transaction_info, latest_receipt_data
    )

    assert transaction.raw_info == transaction_info
    assert transaction.latest_receipt_data == latest_receipt_data


def test_original_transaction_id(transaction_info):
    """
    This property should return the numerical ID of the original
    transaction.
    """
    transaction = subscriptions.AppleTransaction(transaction_info, "foo")

    assert transaction.original_transaction_id == TRANSACTION_ID


def test_product_id(transaction_info):
    """
    If a valid transaction is provided to the container, this property
    should return the product ID from the transaction.
    """
    transaction = subscriptions.AppleTransaction(transaction_info, "foo")

    assert transaction.product_id == PRODUCT_ID
