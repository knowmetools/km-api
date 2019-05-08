from unittest import mock

from rest_framework import status

from apple import views, serializers


@mock.patch("apple.views.generics.CreateAPIView.create", autospec=True)
def test_create(mock_create):
    """
    The create method of the view should take the response output by its
    parent class' ``create`` method and set its status code to 200.
    """
    view = views.ReceiptTypeQueryView()

    response = view.create(None)

    assert response == mock_create.return_value
    assert response.status_code == status.HTTP_200_OK


def test_get_serializer_class():
    """
    Test the serializer class used by the view.
    """
    view = views.ReceiptTypeQueryView()

    assert view.get_serializer_class() == serializers.ReceiptTypeSerializer


def test_perform_create():
    """
    The view's ``perform_create`` method should not save the serializer
    because there's no data to actually save.
    """
    serializer = mock.Mock(name="Mock Serializer")
    view = views.ReceiptTypeQueryView()

    view.perform_create(serializer)

    assert serializer.save.call_count == 0
