import hashlib

from rest_framework import status

from know_me import views


def test_get_hash_does_not_exist(mock_apple_receipt_qs):
    """
    If there is no Apple receipt whose hash matches the one provided,
    the response should have a 404 status code.
    """
    mock_apple_receipt_qs.exists.return_value = False
    data_hash = hashlib.sha256("foo".encode()).hexdigest()

    view = views.AppleReceiptQueryView()
    view.kwargs = {"receipt_hash": data_hash}

    response = view.get(None)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert mock_apple_receipt_qs.filter.call_args[1] == {
        "receipt_data_hash": data_hash
    }


def test_get_hash_exists(mock_apple_receipt_qs):
    """
    If an Apple receipt with the given hash exists, the returned
    response should have a 200 status code.
    """
    mock_apple_receipt_qs.exists.return_value = True
    data_hash = hashlib.sha256("bar".encode()).hexdigest()

    view = views.AppleReceiptQueryView()
    view.kwargs = {"receipt_hash": data_hash}

    response = view.get(None)

    assert response.status_code == status.HTTP_200_OK
    assert mock_apple_receipt_qs.filter.call_args[1] == {
        "receipt_data_hash": data_hash
    }
