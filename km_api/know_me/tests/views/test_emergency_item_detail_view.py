from rest_framework import status

from know_me import models, serializers, views


emergency_item_detail_view = views.EmergencyItemDetailView.as_view()


def test_delete(api_rf, emergency_item_factory):
    """
    Sending a DELETE request to the view should delete the item with the
    given ID.
    """
    item = emergency_item_factory()
    api_rf.user = item.km_user.user

    request = api_rf.delete(item)
    response = emergency_item_detail_view(request, pk=item.pk)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert models.EmergencyItem.objects.count() == 0


def test_get(api_rf, emergency_item_factory):
    """
    Sending a GET request to the view should return the serialized
    details of the item with the given ID.
    """
    item = emergency_item_factory()
    api_rf.user = item.km_user.user

    request = api_rf.get('/')
    response = emergency_item_detail_view(request, pk=item.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.EmergencyItemSerializer(
        item,
        context={'request': request})

    assert response.data == serializer.data


def test_update(api_rf, emergency_item_factory):
    """
    Sending a PATCH request with valid data to the view should update
    the item with the given ID.
    """
    item = emergency_item_factory(name='Old Name')
    api_rf.user = item.km_user.user

    data = {
        'name': 'New Name',
    }

    request = api_rf.patch('/', data)
    response = emergency_item_detail_view(request, pk=item.pk)

    assert response.status_code == status.HTTP_200_OK

    item.refresh_from_db()
    serializer = serializers.EmergencyItemSerializer(
        item,
        context={'request': request})

    assert response.data == serializer.data

    assert item.name == data['name']
