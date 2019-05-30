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


def test_set_cancelled_apple_receipt(
    api_client, apple_receipt_client, user_factory
):
    """
    If a user sends a PUT request with a valid Apple receipt but the
    subscription has been cancelled by Apple's customer support, the
    upload should be rejected.
    """
    expires = timezone.now().replace(microsecond=0) + datetime.timedelta(
        days=30
    )

    # Given John, who is a valid user, is logged in.
    password = "password"
    user = user_factory(first_name="John", password=password)
    api_client.log_in(user.primary_email.email, password)

    # If John has a cancelled receipt...
    receipt_data = "base64-encoded-receipt-data"
    apple_receipt_client.enqueue_status(
        receipt_data,
        {
            "status": 0,
            "latest_receipt": receipt_data,
            "latest_receipt_info": [
                {
                    "cancellation_date": "2019-04-12T23:20:50.52Z",
                    "expires_date_ms": str(int(expires.timestamp() * 1000)),
                    "original_transaction_id": "1",
                    "product_id": PREMIUM_PRODUCT_CODE,
                }
            ],
        },
    )

    # ...then when he sets that receipt as his Know Me subscription...
    data = {"receipt_data": receipt_data}
    response = api_client.put(URL, json=data)

    # ...he should receive a 400 response.
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "receipt_data": ["This subscription has been cancelled by Apple."]
    }


def test_set_duplicate_apple_receipt(
    api_client, apple_receipt_client, apple_receipt_factory, user_factory
):
    """
    If a user attempts to upload a receipt that is already in use, they
    should receive an error message.
    """
    # Assume there is an existing subscription for an Apple receipt.
    expires = timezone.now().replace(microsecond=0) + datetime.timedelta(
        days=30
    )
    receipt = apple_receipt_factory()

    # If Ross is logged in...
    password = "password"
    user = user_factory(first_name="Ross")
    api_client.log_in(user.primary_email.email, password)

    # ...and attempts to upload receipt data that matches the same
    # original transaction as an existing receipt...
    new_receipt_data = "new-receipt-data"
    apple_receipt_client.enqueue_status(
        new_receipt_data,
        {
            "status": 0,
            "latest_receipt": new_receipt_data,
            "latest_receipt_info": [
                {
                    "expires_date_ms": str(int(expires.timestamp() * 1000)),
                    "original_transaction_id": str(receipt.transaction_id),
                    "product_id": PREMIUM_PRODUCT_CODE,
                }
            ],
        },
    )
    data = {"receipt_data": new_receipt_data}
    response = api_client.put(URL, data)

    # ...then he should receive a 400 response with an error indicating
    # the receipt is already in use.
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "receipt_data": ["This receipt has already been used."]
    }


def test_set_expired_apple_receipt(
    api_client, apple_receipt_client, user_factory
):
    """
    If a user uploads an Apple receipt that has expired but is otherwise
    valid, the upload should succeed but their subscription should not
    be activated.

    Regression test for #481.
    """
    expires = timezone.now().replace(microsecond=0)

    # Assume Rebecca is an existing user.
    password = "password"
    user = user_factory(first_name="Rebecca", password=password)
    api_client.log_in(user.primary_email.email, password)

    # If she uploads an expired Apple receipt...
    receipt_data = "expired-receipt"
    apple_receipt_client.enqueue_status(
        receipt_data,
        {
            "status": 0,
            "latest_receipt": receipt_data,
            "latest_receipt_info": [
                {
                    "expires_date_ms": str(int(expires.timestamp()) * 1000),
                    "original_transaction_id": "1234",
                    "product_id": PREMIUM_PRODUCT_CODE,
                }
            ],
        },
    )
    data = {"receipt_data": receipt_data}
    response = api_client.put(URL, data)

    # ...then the upload should succeed but her subscription should not
    # be active.
    assert response.status_code == status.HTTP_200_OK
    assert not api_client.user_has_premium


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
            "latest_receipt": receipt_1,
            "latest_receipt_info": [
                {
                    "expires_date_ms": str(int(expires.timestamp() * 1000)),
                    "original_transaction_id": "1",
                    "product_id": PREMIUM_PRODUCT_CODE,
                }
            ],
        },
    )
    apple_receipt_client.enqueue_status(
        receipt_2,
        {
            "status": 0,
            "latest_receipt": receipt_2,
            "latest_receipt_info": [
                {
                    "expires_date_ms": str(int(expires.timestamp() * 1000)),
                    "original_transaction_id": "2",
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
            "latest_receipt": receipt_data,
            "latest_receipt_info": [
                {
                    "expires_date_ms": str(int(expires.timestamp() * 1000)),
                    "original_transaction_id": "1",
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


def test_set_valid_apple_receipt_activates_subscription(
    api_client, apple_receipt_client, subscription_factory, user_factory
):
    """
    If the user has an existing ``Subscription`` instance that is
    inactive, uploading a new Apple receipt should activate the
    subscription.
    """
    expires = timezone.now().replace(microsecond=0) + datetime.timedelta(
        days=30
    )

    # Given Anne, who is a valid user with an existing subscription, is
    # logged in.
    password = "password"
    user = user_factory(first_name="Anne", password=password)
    api_client.log_in(user.primary_email.email, password)

    subscription_factory(is_active=False, user=user)

    # If Anne has a valid receipt for a recognized product...
    receipt_data = "base64-encoded-receipt-data"
    apple_receipt_client.enqueue_status(
        receipt_data,
        {
            "status": 0,
            "latest_receipt": receipt_data,
            "latest_receipt_info": [
                {
                    "expires_date_ms": str(int(expires.timestamp() * 1000)),
                    "original_transaction_id": "1",
                    "product_id": PREMIUM_PRODUCT_CODE,
                }
            ],
        },
    )

    # ...then when she sets that receipt as her Know Me subscription...
    data = {"receipt_data": receipt_data}
    response = api_client.put(URL, json=data)
    response_data = response.json()

    # ...she should receive a 200 response...
    assert response.status_code == status.HTTP_200_OK
    assert response_data["expiration_time"] == serialized_time(expires)
    assert response_data["receipt_data"] == receipt_data
    assert response_data["receipt_data_hash"] == receipt_data_hash(
        receipt_data
    )

    # ...and her subscription should be set to active.
    response = api_client.get("/know-me/subscription/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["is_active"]
