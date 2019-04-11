import datetime

import pytest
from django.utils import timezone
from rest_framework import status

from test_utils import serialized_time, receipt_data_hash

PREMIUM_PRODUCT_CODE = "premium"
URL = "/know-me/subscription/apple/"


@pytest.fixture(autouse=True)
def set_know_me_premium_product_codes(settings):
    """
    Fixture to automatically set the product code for Know Me Premium.
    """
    settings.APPLE_PRODUCT_CODES["KNOW_ME_PREMIUM"] = [PREMIUM_PRODUCT_CODE]


def test_set_duplicate_apple_receipt(
    api_client, apple_subscription_factory, user_factory
):
    """
    If a user attempts to upload a receipt that is already in use, they
    should receive an error message.
    """
    # Assume there is an existing subscription for an Apple receipt.
    receipt_data = "some-existing-receipt-data"
    apple_subscription_factory(receipt_data=receipt_data)

    # If Ross is logged in...
    password = "password"
    user = user_factory(first_name="Ross")
    api_client.log_in(user.primary_email.email, password)

    # ...and attempts to upload the same receipt data that is already in
    # use...
    data = {"receipt_data": receipt_data}
    response = api_client.put(URL, data)

    # ...then he should receive a 400 response with an error indicating
    # the receipt is already in use.
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "receipt_data": ["This receipt has already been used."]
    }


def test_set_invalid_apple_receipt(
    api_client, apple_receipt_client, user_factory
):
    """
    If a user sends a PUT request with an invalid Apple receipt they
    should receive a 400 response with information about why the receipt
    is invalid.
    """
    # If Rachel is logged in...
    password = "password"
    user = user_factory(first_name="Rachel", password=password)
    api_client.log_in(user.primary_email.email, password)

    # ...and she has some invalid receipt data...
    receipt_data = "invalid-receipt-data"
    apple_receipt_client.enqueue_status(receipt_data, {"status": 21003})

    # ...then when she attempts to set her receipt for her Know Me
    # subscription to an invalid receipt...
    data = {"receipt_data": receipt_data}
    response = api_client.put(URL, json=data)

    # ...she should receive a 400 response.
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_set_multiple_apple_receipts(
    api_client, apple_receipt_client, user_factory
):
    """
    Multiple users should be able to add an Apple receipt to their
    account.

    Regression test for #444
    """
    expires = timezone.now().replace(microsecond=0) + datetime.timedelta(
        days=30
    )
    receipt_1 = "receipt-1"
    receipt_2 = "receipt-2"

    # Given two users, Sarah and John...
    password = "password"
    user1 = user_factory(first_name="Sarah", password=password)
    user2 = user_factory(first_name="John", password=password)

    # ...who both have valid receipts for recognized products...
    apple_receipt_client.enqueue_status(
        receipt_1,
        {
            "status": 0,
            "latest_receipt_info": [
                {
                    "expires_date_ms": str(int(expires.timestamp() * 1000)),
                    "product_id": PREMIUM_PRODUCT_CODE,
                }
            ],
        },
    )
    apple_receipt_client.enqueue_status(
        receipt_2,
        {
            "status": 0,
            "latest_receipt_info": [
                {
                    "expires_date_ms": str(int(expires.timestamp() * 1000)),
                    "product_id": PREMIUM_PRODUCT_CODE,
                }
            ],
        },
    )

    # ...then both of them should be able to set Apple receipts.
    api_client.log_in(user1.primary_email.email, password)
    response = api_client.put(URL, json={"receipt_data": receipt_1})

    assert response.status_code == status.HTTP_200_OK

    api_client.log_in(user2.primary_email.email, password)
    response = api_client.put(URL, json={"receipt_data": receipt_2})

    assert response.status_code == status.HTTP_200_OK


def test_set_valid_apple_receipt(
    api_client, apple_receipt_client, user_factory
):
    """
    If a user sends a PUT request with a valid Apple receipt for a valid
    product the endpoint should return a 200 response.
    """
    expires = timezone.now().replace(microsecond=0) + datetime.timedelta(
        days=30
    )

    # Given Jimmy, who is a valid user, is logged in.
    password = "password"
    user = user_factory(first_name="Jimmy", password=password)
    api_client.log_in(user.primary_email.email, password)

    # If Jimmy has a valid receipt for a recognized product...
    receipt_data = "base64-encoded-receipt-data"
    apple_receipt_client.enqueue_status(
        receipt_data,
        {
            "status": 0,
            "latest_receipt_info": [
                {
                    "expires_date_ms": str(int(expires.timestamp() * 1000)),
                    "product_id": PREMIUM_PRODUCT_CODE,
                }
            ],
        },
    )

    # ...then when he sets that receipt as his Know Me subscription...
    data = {"receipt_data": receipt_data}
    response = api_client.put(URL, json=data)
    response_data = response.json()

    # ...he should receive a 200 response.
    assert response.status_code == status.HTTP_200_OK
    assert response_data["expiration_time"] == serialized_time(expires)
    assert response_data["receipt_data"] == receipt_data
    assert response_data["receipt_data_hash"] == receipt_data_hash(
        receipt_data
    )
