import pytest

from rest_framework import status

from know_me.profile import serializers


@pytest.mark.integration
def test_create_media_resource(
        api_client,
        api_rf,
        file,
        km_user_factory):
    """
    Sending a POST request to the view should create a new media
    resource for the specified user.
    """
    km_user = km_user_factory()

    api_client.force_authenticate(user=km_user.user)
    api_rf.user = km_user.user

    data = {
        'file': file,
        'name': 'Test Media Resource',
    }

    url = km_user.get_media_resource_list_url()
    request = api_rf.post(url, data)
    file.seek(0)
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = serializers.MediaResourceSerializer(
        km_user.media_resources.get(),
        context={'request': request})

    assert response.data == serializer.data


@pytest.mark.integration
def test_get_media_resource_list(
        api_client,
        api_rf,
        km_user_factory,
        media_resource_factory):
    """
    Sending a GET request to the view should return a list of the media
    resources that belong to the specified Know Me user.
    """
    km_user = km_user_factory()

    api_client.force_authenticate(user=km_user.user)
    api_rf.user = km_user.user

    media_resource_factory(km_user=km_user)
    media_resource_factory(km_user=km_user)
    media_resource_factory()

    url = km_user.get_media_resource_list_url()
    request = api_rf.get(url)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.MediaResourceSerializer(
        km_user.media_resources.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data
