from unittest import mock

import pytest
from django.http import Http404

from know_me import models, views
from know_me.serializers import subscription_serializers


def test_get_object_does_not_exist(mock_apple_receipt_qs):
    """
    If there is no receipt with the given data hash, an ``Http404``
    exception should be raised.
    """
    data_hash = models.AppleReceipt.hash_data("foo")
    mock_apple_receipt_qs.get.side_effect = models.AppleReceipt.DoesNotExist

    view = views.AppleReceiptQueryView()
    view.kwargs = {"receipt_hash": data_hash}

    with pytest.raises(Http404):
        view.get_object()


def test_get_object_exists(mock_apple_receipt_qs):
    """
    If there is an Apple receipt with the given hash, it should be
    returned.
    """
    receipt = mock.Mock(name="Mock Receipt")
    receipt.receipt_data_hash = models.AppleReceipt.hash_data("foo")
    mock_apple_receipt_qs.get.return_value = receipt

    view = views.AppleReceiptQueryView()
    view.kwargs = {"receipt_hash": receipt.receipt_data_hash}

    assert view.get_object() == receipt
    assert mock_apple_receipt_qs.get.call_args[1] == {
        "receipt_data_hash": receipt.receipt_data_hash
    }


def test_get_serializer_class():
    """
    Test the serializer class used by the view.
    """
    expected = subscription_serializers.AppleReceiptQuerySerializer
    view = views.AppleReceiptQueryView()

    assert view.get_serializer_class() == expected
