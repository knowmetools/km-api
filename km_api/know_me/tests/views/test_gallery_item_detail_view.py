from rest_framework import status

from know_me import serializers, views


gallery_item_detail_view = views.GalleryItemDetailView.as_view()


def test_get_gallery_item(api_rf, gallery_item_factory):
    """
    Users should be able to get the details of a gallery item that
    belongs to their own profile.
    """
    item = gallery_item_factory()
    profile = item.profile

    api_rf.user = profile.user

    request = api_rf.get(profile.get_absolute_url())
    response = gallery_item_detail_view(
        request,
        gallery_item_pk=item.pk,
        profile_pk=profile.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.GalleryItemSerializer(
        item,
        context={'request': request})

    assert response.data == serializer.data


def test_update_gallery_item(api_rf, gallery_item_factory):
    """
    Sending a PATCH request to the view with valid data should update
    the given gallery item.
    """
    item = gallery_item_factory(name='Old Name')
    profile = item.profile

    api_rf.user = profile.user

    data = {
        'name': 'New Name',
    }

    request = api_rf.patch(profile.get_absolute_url(), data)
    response = gallery_item_detail_view(
        request,
        gallery_item_pk=item.pk,
        profile_pk=profile.pk)

    assert response.status_code == status.HTTP_200_OK

    item.refresh_from_db()
    serializer = serializers.GalleryItemSerializer(
        item,
        context={'request': request})

    assert response.data == serializer.data
    assert item.name == data['name']
