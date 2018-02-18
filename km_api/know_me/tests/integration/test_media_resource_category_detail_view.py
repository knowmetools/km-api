import pytest

from rest_framework import status
from rest_framework.reverse import reverse

from know_me import models, serializers


@pytest.mark.integration
def test_delete_media_resource_category(
        api_client,
        media_resource_category_factory):
    """
    Sending a DELETE request to the view should delete the category with
    the given ID.
    """
    category = media_resource_category_factory()
    api_client.force_authenticate(user=category.km_user.user)

    url = reverse(
        'know-me:media-resource-category-detail',
        kwargs={'pk': category.pk})
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert models.MediaResourceCategory.objects.count() == 0


@pytest.mark.integration
def test_retrieve_media_resource_category(
        api_client,
        media_resource_category_factory):
    """
    Sending a GET request to the view should return the details of the
    category with the given ID.
    """
    category = media_resource_category_factory()
    api_client.force_authenticate(user=category.km_user.user)

    url = reverse(
        'know-me:media-resource-category-detail',
        kwargs={'pk': category.pk})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.MediaResourceCategorySerializer(category)

    assert response.data == serializer.data


@pytest.mark.integration
def test_update_media_resource_category(
        api_client,
        media_resource_category_factory):
    """
    Sending a PATCH request to the view should update the category with
    the given ID.
    """
    category = media_resource_category_factory(name='Old Name')
    api_client.force_authenticate(user=category.km_user.user)

    data = {
        'name': 'New Name',
    }

    url = reverse(
        'know-me:media-resource-category-detail',
        kwargs={'pk': category.pk})
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK

    category.refresh_from_db()

    assert category.name == data['name']
