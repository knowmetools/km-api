import pytest

from rest_framework import status

from know_me.profile import models, serializers


@pytest.mark.integration
def test_attach_media_resource(
    api_client, media_resource_factory, profile_item_factory
):
    """
    Attaching a media resource to a profile item should not raise an
    exception.

    Regression test for #317.
    """
    resource = media_resource_factory()
    item = profile_item_factory(topic__profile__km_user=resource.km_user)

    api_client.force_authenticate(user=resource.km_user.user)

    data = {"media_resource_id": resource.id}

    url = item.get_absolute_url()
    response = api_client.patch(url, data)

    item.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert item.media_resource == resource


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
def test_detach_media_resource(
    api_client, media_resource_factory, profile_item_factory
):
    """
    Sending a null value for the media resource attached to a profile
    item should detach any media resource from the specified profile
    item.

    Regression test for #321
    """
    resource = media_resource_factory()
    item = profile_item_factory(
        media_resource=resource, topic__profile__km_user=resource.km_user
    )

    api_client.force_authenticate(user=resource.km_user.user)

    data = {"media_resource_id": ""}

    url = item.get_absolute_url()
    response = api_client.patch(url, data)

    item.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK, response.data
    assert item.media_resource is None


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
        item, context={"request": request}
    )

    assert response.data == serializer.data


@pytest.mark.integration
def test_update_profile_item(api_client, profile_item_factory):
    """
    Sending a PATCH request to the view should update the specified
    profile item's information.
    """
    item = profile_item_factory(name="Old Name")
    api_client.force_authenticate(user=item.topic.profile.km_user.user)

    data = {"name": "New Name"}

    url = item.get_absolute_url()
    response = api_client.patch(url, data)

    item.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert item.name == data["name"]
