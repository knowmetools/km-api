from rest_framework import status
from rest_framework.reverse import reverse

from know_me import serializers


def test_create_media_resource(api_client, api_rf, file, km_user_factory):
    """
    Sending a POST request with valid data to the view should create a
    new media resource for the specified user.
    """
    km_user = km_user_factory()

    api_client.force_authenticate(user=km_user.user)
    api_rf.user = km_user.user

    data = {
        'file': file,
        'name': 'Foo',
    }

    url = reverse('know-me:media-resource-list', kwargs={'pk': km_user.pk})
    request = api_rf.post(url, data)
    # We have to seek back to the beginning because the above line moves
    # the file's pointer to the end.
    file.seek(0)
    response = api_client.post(url, data, format='multipart')

    assert response.status_code == status.HTTP_201_CREATED, response.data

    serializer = serializers.MediaResourceSerializer(
        km_user.media_resources.get(),
        context={'request': request})

    assert response.data == serializer.data


def test_create_media_resource_shared_user(
        api_client,
        api_rf,
        file,
        km_user_accessor_factory,
        km_user_factory,
        user_factory):
    """
    Sending a POST request with valid data to the view as a user who has
    been granted shared write access should create a new media resource.
    """
    km_user = km_user_factory()
    user = user_factory()
    km_user_accessor_factory(
        km_user=km_user,
        accepted=True,
        can_write=True,
        user_with_access=user)

    api_client.force_authenticate(user=user)
    api_rf.user = user

    data = {
        'file': file,
        'name': 'Foo',
    }

    url = reverse('know-me:media-resource-list', kwargs={'pk': km_user.pk})
    request = api_rf.post(url, data)
    # We have to seek back to the beginning because the above line moves
    # the file's pointer to the end.
    file.seek(0)
    response = api_client.post(url, data, format='multipart')

    assert response.status_code == status.HTTP_201_CREATED, response.data

    serializer = serializers.MediaResourceSerializer(
        km_user.media_resources.get(),
        context={'request': request})

    assert response.data == serializer.data


def test_create_media_resource_unauthorized(
        api_client,
        api_rf,
        file,
        km_user_factory,
        user_factory):
    """
    Users who have not been granted write access to a Know Me user's
    account should not be able to upload media resources for them.
    """
    km_user = km_user_factory()
    user = user_factory()

    api_client.force_authenticate(user=user)
    api_rf.user = user

    data = {
        'file': file,
        'name': 'Foo',
    }

    url = reverse('know-me:media-resource-list', kwargs={'pk': km_user.pk})
    response = api_client.post(url, data, format='multipart')

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_anonymous(api_client, km_user_factory):
    """
    Sending a GET request to the view as an anonymous user should return
    a permissions error.
    """
    km_user = km_user_factory()

    url = reverse('know-me:media-resource-list', kwargs={'pk': km_user.pk})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_filtered_list(
        api_client,
        api_rf,
        km_user_factory,
        media_resource_category_factory,
        media_resource_factory):
    """
    If a category is specified, only media resources belonging to that
    category should be returned.
    """
    km_user = km_user_factory()
    category = media_resource_category_factory(km_user=km_user)

    media_resource_factory(category=category, km_user=km_user)
    media_resource_factory(category=category, km_user=km_user)

    media_resource_factory(km_user=km_user)

    api_client.force_authenticate(user=km_user.user)
    api_rf.user = km_user.user

    url = reverse('know-me:media-resource-list', kwargs={'pk': km_user.pk})
    request = api_rf.get(url)
    response = api_client.get(url, {'category': category.pk})

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.MediaResourceSerializer(
        category.media_resources.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data


def test_get_media_resource_list(
        api_client,
        api_rf,
        km_user_factory,
        media_resource_factory):
    """
    Sending a GET request to the view as an authorized user should
    return a list of the media resources owned by the specified user.
    """
    km_user = km_user_factory()

    media_resource_factory(km_user=km_user)
    media_resource_factory(km_user=km_user)

    api_client.force_authenticate(user=km_user.user)
    api_rf.user = km_user.user

    url = reverse('know-me:media-resource-list', kwargs={'pk': km_user.pk})
    request = api_rf.get(url)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.MediaResourceSerializer(
        km_user.media_resources.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data
