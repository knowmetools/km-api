import hashlib

from rest_framework import status

from know_me import views


def test_get_hash_does_not_exist(db):
    """
    If there is no Apple receipt whose hash matches the one provided,
    the response should have a 404 status code.
    """
    data_hash = hashlib.sha256("foo".encode()).hexdigest()

    view = views.AppleReceiptQueryView()
    view.kwargs = {"receipt_hash": data_hash}

    response = view.get(None)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_hash_exists(apple_subscription_factory):
    """
    If an Apple receipt with the given hash exists, the returned
    response should have a 200 status code.
    """
    receipt = apple_subscription_factory()

    view = views.AppleReceiptQueryView()
    view.kwargs = {"receipt_hash": receipt.receipt_data_hash}

    response = view.get(None)

    assert response.status_code == status.HTTP_200_OK
