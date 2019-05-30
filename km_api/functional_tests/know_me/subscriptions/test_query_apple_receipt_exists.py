import pytest
from rest_framework import status


PREMIUM_PRODUCT_CODE = "premium"
URL = "/know-me/subscription/apple/query/"


@pytest.fixture(autouse=True)
def set_know_me_premium_product_codes(settings):
    """
    Fixture to automatically set the product code for Know Me Premium.
    """
    settings.APPLE_PRODUCT_CODES["KNOW_ME_PREMIUM"] = [PREMIUM_PRODUCT_CODE]


def test_apple_receipt_does_not_exist(
    api_client, apple_receipt_client, apple_receipt_factory
):
    """
    If there is no existing Apple receipt with the same transaction ID
    as the receipt identified by the provided data, the query should
    indicate that the receipt is not in use.
    """
    # If there is a valid receipt...
    receipt_data = "foo"
    apple_receipt_client.enqueue_status(
        receipt_data,
        {
            "latest_receipt": receipt_data,
            "latest_receipt_info": [
                {
                    "original_transaction_id": "bar",
                    "product_id": PREMIUM_PRODUCT_CODE,
                }
            ],
            "status": 0,
        },
    )

    # ...then querying with that receipt data should indicate the
    # receipt is not used.
    response = api_client.post(URL, {"receipt_data": receipt_data})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"email": None, "is_used": False}


def test_apple_receipt_exists(
    api_client, apple_receipt_client, apple_receipt_factory
):
    """
    If an Apple receipt with the same original transaction ID as the
    receipt passed to the endpoint exists, the endpoint should return
    the primary email address of the user who owns the receipt.
    """
    # Assume there is an existing Apple receipt.
    receipt = apple_receipt_factory()

    # If there is a receipt that matches to the same transaction ID...
    receipt_data = "foo"
    apple_receipt_client.enqueue_status(
        receipt_data,
        {
            "latest_receipt": receipt_data,
            "latest_receipt_info": [
                {
                    "original_transaction_id": str(receipt.transaction_id),
                    "product_id": PREMIUM_PRODUCT_CODE,
                }
            ],
            "status": 0,
        },
    )

    # ...then querying with that receipt data should return the email
    # address of the original receipt's owner.
    response = api_client.post(URL, {"receipt_data": receipt_data})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "email": receipt.subscription.user.primary_email.email,
        "is_used": True,
    }


def test_wrong_endpoint(api_client):
    """
    Attempting to query using the wrong endpoint should return a 404
    response.

    Regression test for #505.
    """
    response = api_client.post("/know-me/subscription/apple/foobar/", {})

    assert response.status_code == status.HTTP_404_NOT_FOUND
