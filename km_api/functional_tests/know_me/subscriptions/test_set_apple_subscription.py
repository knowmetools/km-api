import pytest
from rest_framework import status
from rest_framework.reverse import reverse


PREMIUM_PRODUCT_CODE = "premium"


@pytest.fixture(autouse=True)
def set_know_me_premium_product_codes(settings):
    """
    Fixture to automatically set the product code for Know Me Premium.
    """
    settings.APPLE_PRODUCT_CODES["KNOW_ME_PREMIUM"] = [PREMIUM_PRODUCT_CODE]


def test_set_invalid_apple_receipt(
    api_client, apple_receipt_client, email_factory, user_factory
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
    url = reverse("know-me:apple-subscription-detail")
    response = api_client.put(url, json=data)

    # ...she should receive a 400 response.
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_set_valid_apple_receipt(
    api_client, apple_receipt_client, email_factory, user_factory
):
    """
    If a user sends a PUT request with a valid Apple receipt for a valid
    product the endpoint should return a 200 response.
    """
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
            "latest_receipt_info": [{"product_id": PREMIUM_PRODUCT_CODE}],
        },
    )

    # ...then when he sets that receipt as his Know Me subscription...
    data = {"receipt_data": receipt_data}
    url = reverse("know-me:apple-subscription-detail")
    response = api_client.put(url, json=data)
    response_data = response.json()

    # ...he should receive a 200 response.
    assert response.status_code == status.HTTP_200_OK
    assert response_data["receipt_data"] == receipt_data
