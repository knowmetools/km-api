import pytest

from rest_framework import status

from know_me.profile import models, serializers


@pytest.mark.integration
def test_delete_media_resource(api_client, media_resource_factory):
    """
    Sending a DELETE request to the view should delete the specified
    media resource.
    """
    resource = media_resource_factory()
    api_client.force_authenticate(user=resource.km_user.user)

    url = resource.get_absolute_url()
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert models.MediaResource.objects.count() == 0


@pytest.mark.integration
def test_get_media_resource(api_client, api_rf, media_resource_factory):
    """
    Sending a GET request to the view should return the details of the
    specified media resource.
    """
    resource = media_resource_factory()

    api_client.force_authenticate(user=resource.km_user.user)
    api_rf.user = resource.km_user.user

    url = resource.get_absolute_url()
    request = api_rf.get(url)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.MediaResourceSerializer(
        resource, context={"request": request}
    )

    assert response.data == serializer.data


@pytest.mark.integration
def test_update_media_resource(api_client, media_resource_factory):
    """
    Sending a PATCH request to the view should update the specified
    media resource with the provided information.
    """
    resource = media_resource_factory(name="Old Name")
    api_client.force_authenticate(user=resource.km_user.user)

    data = {"name": "New Name"}

    url = resource.get_absolute_url()
    response = api_client.patch(url, data)

    resource.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert resource.name == data["name"]
