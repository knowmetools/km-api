import pytest

from rest_framework import status

from know_me.profile import serializers


@pytest.mark.integration
def test_create_profile(api_client, api_rf, km_user_factory):
    """
    Sending a POST request to the view should create a new profile for
    the specified Know Me user.
    """
    km_user = km_user_factory()

    api_client.force_authenticate(user=km_user.user)
    api_rf.user = km_user.user

    data = {
        'name': 'Test Profile',
    }

    url = km_user.get_profile_list_url()
    request = api_rf.post(url, data)
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = serializers.ProfileListSerializer(
        km_user.profiles.get(),
        context={'request': request})

    assert response.data == serializer.data


@pytest.mark.integration
def test_get_profile_list(
        api_client,
        api_rf,
        km_user_factory,
        profile_factory):
    """
    Sending a GET request to the view should return a list of profiles
    accessible to the requesting user.
    """
    km_user = km_user_factory()

    api_client.force_authenticate(user=km_user.user)
    api_rf.user = km_user.user

    profile_factory(km_user=km_user)
    profile_factory(km_user=km_user)
    profile_factory()

    url = km_user.get_profile_list_url()
    request = api_rf.get(url)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ProfileListSerializer(
        km_user.profiles.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data
