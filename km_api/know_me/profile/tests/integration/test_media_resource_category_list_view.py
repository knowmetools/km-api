import pytest

from rest_framework import status

from know_me.profile import serializers


@pytest.mark.integration
def test_create_media_resource_category(api_client, api_rf, km_user_factory):
    """
    Sending a POST request to the view should create a new media
    resource category.
    """
    km_user = km_user_factory()

    api_client.force_authenticate(user=km_user.user)
    api_rf.user = km_user.user

    data = {"name": "Test Category"}

    url = km_user.get_media_resource_category_list_url()
    request = api_rf.post(url, data)
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = serializers.MediaResourceCategorySerializer(
        km_user.media_resource_categories.get(), context={"request": request}
    )

    assert response.data == serializer.data


@pytest.mark.integration
def test_list_media_resource_categories(
    api_client, api_rf, km_user_factory, media_resource_category_factory
):
    """
    Sending a GET request to the view should list the media resource
    categories accessible to that user.
    """
    km_user = km_user_factory()

    api_client.force_authenticate(user=km_user.user)
    api_rf.user = km_user.user

    media_resource_category_factory(km_user=km_user)
    media_resource_category_factory(km_user=km_user)
    media_resource_category_factory()

    url = km_user.get_media_resource_category_list_url()
    request = api_rf.get(url)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.MediaResourceCategorySerializer(
        km_user.media_resource_categories.all(),
        context={"request": request},
        many=True,
    )

    assert response.data == serializer.data
