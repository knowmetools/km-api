import hashlib

from rest_framework import status


def test_apple_receipt_does_not_exist(api_client):
    """
    If there is no Apple receipt whose data hashes to the specified
    value then a 404 response should be returned.
    """
    data_hash = hashlib.sha256("foo".encode()).hexdigest()
    url = f"/know-me/subscription/apple/{data_hash}/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_apple_receipt_exists(api_client, apple_subscription_factory):
    """
    If an Apple subscription whose receipt data matches the provided
    hash exists, a 200 response should be returned.
    """
    # Assume an Apple receipt for some user exists.
    apple_receipt = apple_subscription_factory()

    # Querying for that receipt by its hash should return a 200 response
    # indicating it exists.
    url = f"/know-me/subscription/apple/{apple_receipt.receipt_data_hash}/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
