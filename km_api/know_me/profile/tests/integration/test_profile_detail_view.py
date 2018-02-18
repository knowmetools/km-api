import pytest

from rest_framework import status

from know_me.profile import models, serializers


@pytest.mark.integration
def test_delete_profile(api_client, profile_factory):
    """
    Sending a DELETE request to the view should delete the specified
    profile.
    """
    profile = profile_factory()
    api_client.force_authenticate(user=profile.km_user.user)

    url = profile.get_absolute_url()
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert models.Profile.objects.count() == 0


@pytest.mark.integration
def test_get_profile(api_client, api_rf, profile_factory):
    """
    Sending a GET request to the view should return the specified
    profile's information.
    """
    profile = profile_factory()

    api_client.force_authenticate(user=profile.km_user.user)
    api_rf.user = profile.km_user.user

    url = profile.get_absolute_url()
    request = api_rf.get(url)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ProfileDetailSerializer(
        profile,
        context={'request': request})

    assert response.data == serializer.data


@pytest.mark.integration
def test_update_profile(api_client, profile_factory):
    """
    Sending a PATCH request to the view should update the specified
    profile's information.
    """
    profile = profile_factory(name='Old Name')
    api_client.force_authenticate(user=profile.km_user.user)

    data = {
        'name': 'New Name',
    }

    url = profile.get_absolute_url()
    response = api_client.patch(url, data)

    profile.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert profile.name == data['name']
