from unittest import mock

import pytest
from rest_framework.exceptions import ValidationError as DRFValidationError

from apple import serializers
from apple.receipts import ReceiptCodes


@mock.patch("apple.serializers.receipts.get_receipt_info", autospec=True)
def test_validate_invalid_receipt(mock_get_info):
    """
    If a receipt is invalid, an exception should be raised.
    """
    receipt_data = "foo"
    mock_get_info.return_value = {"status": ReceiptCodes.COULD_NOT_AUTHORIZE}

    serializer = serializers.ReceiptTypeSerializer()

    with pytest.raises(DRFValidationError):
        serializer.validate({"receipt_data": receipt_data})


@mock.patch("apple.serializers.receipts.get_receipt_info", autospec=True)
def test_validate_production_receipt_from_sandbox(mock_get_info):
    """
    If a receipt is valid in the production environment and we are
    querying the sandbox endpoint, running the serializer validation
    should  set ``environment`` to ``PRODUCTION``.
    """
    receipt_data = "foo"
    mock_get_info.return_value = {"status": ReceiptCodes.PRODUCTION_RECEIPT}

    serializer = serializers.ReceiptTypeSerializer()
    validated = serializer.validate({"receipt_data": receipt_data})

    assert mock_get_info.call_args[0] == (receipt_data,)
    assert validated["environment"] == "PRODUCTION"


@mock.patch("apple.serializers.receipts.get_receipt_info", autospec=True)
def test_validate_sandbox_receipt_from_production(mock_get_info):
    """
    If a receipt is valid in the sandbox environment and we are querying
    the production endpoint, running the serializer validation should
    set ``environment`` to ``SANDBOX``.
    """
    receipt_data = "foo"
    mock_get_info.return_value = {"status": ReceiptCodes.TEST_RECEIPT}

    serializer = serializers.ReceiptTypeSerializer()
    validated = serializer.validate({"receipt_data": receipt_data})

    assert mock_get_info.call_args[0] == (receipt_data,)
    assert validated["environment"] == "SANDBOX"


@mock.patch("apple.serializers.receipts.get_receipt_info", autospec=True)
def test_validate_valid_receipt_from_production(mock_get_info, settings):
    """
    If we are validating against the production endpoint and the receipt
    comes back valid, the ``environment`` should be set to
    ``PRODUCTION``.
    """
    # Pretend that the endpoint we are using is the production endpoint.
    endpoint = settings.APPLE_RECEIPT_VALIDATION_ENDPOINT
    settings.APPLE_RECEIPT_VALIDATION_PRODUCTION_ENDPOINT = endpoint

    # Validation should indicate the receipt is from the production
    # environment.
    receipt_data = "foo"
    mock_get_info.return_value = {"status": ReceiptCodes.VALID}

    serializer = serializers.ReceiptTypeSerializer()
    validated = serializer.validate({"receipt_data": receipt_data})

    assert mock_get_info.call_args[0] == (receipt_data,)
    assert validated["environment"] == "PRODUCTION"


@mock.patch("apple.serializers.receipts.get_receipt_info", autospec=True)
def test_validate_valid_receipt_from_sandbox(mock_get_info, settings):
    """
    If we are validating against the sandbox endpoint and the receipt
    comes back valid, the ``environment`` should be set to ``SANDBOX``.
    """
    # Pretend that the endpoint we are using is the sandbox endpoint.
    prod_endpoint = "http://fake.production.endpoint.example.com"
    settings.APPLE_RECEIPT_VALIDATION_PRODUCTION_ENDPOINT = prod_endpoint

    # Validation should indicate the receipt is from the sandbox
    # environment.
    receipt_data = "foo"
    mock_get_info.return_value = {"status": ReceiptCodes.VALID}

    serializer = serializers.ReceiptTypeSerializer()
    validated = serializer.validate({"receipt_data": receipt_data})

    assert mock_get_info.call_args[0] == (receipt_data,)
    assert validated["environment"] == "SANDBOX"
