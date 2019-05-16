from unittest import mock

from rest_framework import status

from know_me import views
from know_me.serializers import subscription_serializers


@mock.patch("know_me.views.generics.CreateAPIView.create", autospec=True)
def test_create(mock_create):
    """
    The create method of the view should take the response output by its
    parent class' ``create`` method and set its status code to 200.
    """
    view = views.AppleReceiptQueryView()

    response = view.create(None)

    assert response == mock_create.return_value
    assert response.status_code == status.HTTP_200_OK


def test_get_serializer_class():
    """
    Test the serializer class used by the view.
    """
    expected = subscription_serializers.AppleReceiptQuerySerializer
    view = views.AppleReceiptQueryView()

    assert view.get_serializer_class() == expected
