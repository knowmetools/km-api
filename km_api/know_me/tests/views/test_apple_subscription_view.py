from unittest import mock

import pytest
from django.http import Http404

from know_me import views, models


@pytest.fixture
def mock_apple_receipt_qs():
    mock_queryset = mock.Mock(spec=models.AppleReceipt.objects)
    mock_queryset.all.return_value = mock_queryset
    mock_queryset.model.DoesNotExist = models.AppleReceipt.DoesNotExist

    with mock.patch(
        "know_me.models.AppleReceipt.objects", new=mock_queryset
    ), mock.patch(
        "know_me.models.AppleReceipt._meta.default_manager", new=mock_queryset
    ):
        yield mock_queryset


def test_get_object_exists(mock_apple_receipt_qs):
    """
    If there is an Apple receipt for the requesting user, it should be
    returned.
    """
    receipt = mock.Mock(name="Mock Receipt")
    mock_apple_receipt_qs.get.return_value = receipt
    request = mock.Mock(name="Mock Request")
    request.user = receipt.subscription.user

    view = views.AppleSubscriptionView()
    view.request = request

    assert view.get_object() == receipt
    assert mock_apple_receipt_qs.get.call_args[1] == {
        "subscription__user": receipt.subscription.user
    }


def test_get_object_missing(mock_apple_receipt_qs):
    """
    If the requesting user has no Apple subscription, an ``Http404``
    should be thrown for a ``GET`` request.
    """
    mock_apple_receipt_qs.get.side_effect = models.AppleReceipt.DoesNotExist
    request = mock.Mock(name="Mock Request")

    view = views.AppleSubscriptionView()
    view.request = request

    with pytest.raises(Http404):
        view.get_object()


def test_perform_destroy():
    """
    Destroying an Apple receipt should also deactivate the parent
    subscription.
    """
    receipt = mock.Mock(name="Mock Receipt")
    receipt.subscription.is_active = True
    receipt.subscription.pk = 42

    view = views.AppleSubscriptionView()
    view.perform_destroy(receipt)

    assert receipt.delete.call_count == 1
    assert not receipt.subscription.is_active
    assert receipt.subscription.save.call_count == 1
