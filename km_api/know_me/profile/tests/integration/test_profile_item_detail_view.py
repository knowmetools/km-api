import pytest

from rest_framework import status

from know_me.profile import models, serializers


@pytest.mark.integration
def test_delete_profile_item(api_client, profile_item_factory):
    """
    Sending a DELETE request to the view should delete the profile item
    with the specified ID.
    """
    item = profile_item_factory()
    api_client.force_authenticate(user=item.topic.profile.km_user.user)

    url = item.get_absolute_url()
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert models.ProfileItem.objects.count() == 0


@pytest.mark.integration
def test_get_profile_item(api_client, api_rf, profile_item_factory):
    """
    Sending a GET request to the view should return the information of
    the specified profile item.
    """
    item = profile_item_factory()
    user = item.topic.profile.km_user.user

    api_client.force_authenticate(user=user)
    api_rf.user = user

    url = item.get_absolute_url()
    request = api_rf.get(url)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ProfileItemDetailSerializer(
        item,
        context={'request': request})

    assert response.data == serializer.data


@pytest.mark.integration
def test_update_profile_item(api_client, profile_item_factory):
    """
    Sending a PATCH request to the view should update the specified
    profile item's information.
    """
    item = profile_item_factory(name='Old Name')
    api_client.force_authenticate(user=item.topic.profile.km_user.user)

    data = {
        'name': 'New Name',
    }

    url = item.get_absolute_url()
    response = api_client.patch(url, data)

    item.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert item.name == data['name']
