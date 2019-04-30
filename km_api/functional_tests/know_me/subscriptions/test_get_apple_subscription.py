from rest_framework import status
from rest_framework.reverse import reverse

from test_utils import serialized_time, receipt_data_hash

URL = reverse("know-me:apple-subscription-detail")


def test_get_anonymous(api_client):
    """
    Anonymous users should receive a permissions error if they send a
    GET request to the view.
    """
    response = api_client.get(URL)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_existing_subscription(
    api_client, apple_receipt_factory, user_factory
):
    """
    Users should be able to fetch information about their existing
    Apple subscription.
    """
    # Given James, an authenticated user...
    password = "password"
    user = user_factory(first_name="James", password=password)
    api_client.log_in(user.primary_email.email, password)

    # ...who has an existing Apple receipt...
    receipt = apple_receipt_factory(subscription__user=user)

    # ...then he should be able to view information about his Apple
    # receipt.
    response = api_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "expiration_time": serialized_time(receipt.expiration_time),
        "id": str(receipt.pk),
        "receipt_data": receipt.receipt_data,
        "receipt_data_hash": receipt_data_hash(receipt.receipt_data),
        "time_created": serialized_time(receipt.time_created),
        "time_updated": serialized_time(receipt.time_updated),
    }
