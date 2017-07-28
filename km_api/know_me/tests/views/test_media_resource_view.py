from rest_framework import status

from know_me import serializers, views


media_resource_detail_view = views.MediaResourceDetailView.as_view()


def test_get_media_resource(api_rf, media_resource_factory):
    """
    Users should be able to get the details of a media resource that
    belongs to their own profile.
    """
    resource = media_resource_factory()
    profile = resource.profile

    api_rf.user = profile.user

    request = api_rf.get(profile.get_absolute_url())
    response = media_resource_detail_view(request, pk=resource.pk)
    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.MediaResourceSerializer(
        resource,
        context={'request': request})

    assert response.data == serializer.data


def test_update_media_resource(api_rf, media_resource_factory):
    """
    Sending a PATCH request to the view with valid data should update
    the given media resource.
    """
    resource = media_resource_factory(name='Old Name')
    profile = resource.profile

    api_rf.user = profile.user

    data = {
        'name': 'New Name',
    }

    request = api_rf.patch(profile.get_absolute_url(), data)
    response = media_resource_detail_view(request, pk=resource.pk)
    assert response.status_code == status.HTTP_200_OK

    resource.refresh_from_db()
    serializer = serializers.MediaResourceSerializer(
        resource,
        context={'request': request})

    assert response.data == serializer.data
    assert resource.name == data['name']
