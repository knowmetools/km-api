from rest_framework import status

from know_me import serializers, views


emergency_item_list_view = views.EmergencyItemListView.as_view()


def test_create(api_rf, km_user_factory):
    """
    Sending a POST request with valid data to the view should create a
    new emergency item for the requesting user.
    """
    km_user = km_user_factory()
    api_rf.user = km_user.user

    data = {
        'name': 'Test Emergency Item',
    }

    request = api_rf.post(km_user.get_emergency_item_list_url(), data)
    response = emergency_item_list_view(request, pk=km_user.pk)

    assert response.status_code == status.HTTP_201_CREATED


def test_get(api_rf, emergency_item_factory, km_user_factory):
    """
    Sending a GET request to the view should return a list of all the
    emergency items owned by Know Me user specified.
    """
    km_user = km_user_factory()
    emergency_item_factory(km_user=km_user)
    emergency_item_factory(km_user=km_user)

    api_rf.user = km_user.user

    request = api_rf.get(km_user.get_emergency_item_list_url())
    response = emergency_item_list_view(request, pk=km_user.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.EmergencyItemSerializer(
        km_user.emergency_items.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data
