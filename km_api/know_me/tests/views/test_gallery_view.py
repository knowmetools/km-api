from rest_framework import status

from know_me import serializers, views


gallery_view = views.GalleryView.as_view()


def test_create(api_rf, file, profile_factory):
    """
    Sending a POST request to the view containing valid data should
    create a new media resource.
    """
    profile = profile_factory()

    api_rf.user = profile.user

    data = {
        'name': 'Test Media Resource',
        'file': file,
    }

    request = api_rf.post(profile.get_gallery_url(), data)
    response = gallery_view(request, pk=profile.pk)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = serializers.MediaResourceSerializer(
        profile.media_resources.get(),
        context={'request': request})

    assert response.data == serializer.data
