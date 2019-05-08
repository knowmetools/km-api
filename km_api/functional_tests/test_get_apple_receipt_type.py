from rest_framework import status


URL = "/apple/receipt-type-query/"


def test_get_receipt_type_invalid(api_client, apple_receipt_client):
    """
    If the provided Apple receipt is invalid, the endpoint should return
    an error.
    """
    # Assuming some receipt data maps to an invalid receipt...
    receipt_data = "foobar"
    apple_receipt_client.enqueue_status(receipt_data, {"status": 21010})

    # ...then the type check endpoint should return an error response.
    response = api_client.post(URL, {"receipt_data": receipt_data})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "receipt_data": ["The provided receipt is invalid."]
    }


def test_get_receipt_type_production(
    api_client, apple_receipt_client, settings
):
    """
    If the provided Apple receipt is valid in the production environment
    then the environment should be set to ``PRODUCTION``.
    """
    # Pretend that the endpoint we are using is the production endpoint.
    endpoint = settings.APPLE_RECEIPT_VALIDATION_ENDPOINT
    settings.APPLE_RECEIPT_VALIDATION_PRODUCTION_ENDPOINT = endpoint

    # Assuming some set of receipt data maps to a valid production
    # receipt...
    receipt_data = "foobar"
    apple_receipt_client.enqueue_status(receipt_data, {"status": 0})

    # ...the type check endpoint should return that the receipt belongs
    # to the production environment.
    response = api_client.post(URL, {"receipt_data": receipt_data})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"environment": "PRODUCTION"}


def test_get_receipt_type_sandbox(api_client, apple_receipt_client):
    """
    If the provided Apple receipt is from the sandbox environment then
    the ``environment`` key of the response should be set to
    ``SANDBOX``.
    """
    # Assuming some receipt data maps to a valid sandbox receipt...
    receipt_data = "foobar"
    apple_receipt_client.enqueue_status(receipt_data, {"status": 21007})

    # ...then the type check endpoint should return that the receipt is
    # from the test environment.
    response = api_client.post(URL, {"receipt_data": receipt_data})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"environment": "SANDBOX"}
