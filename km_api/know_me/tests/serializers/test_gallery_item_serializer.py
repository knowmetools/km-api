from know_me import serializers


def test_create(file, profile_factory):
    """
    Saving a serializer containing valid data should create a new
    gallery item attached to the given profile.
    """
    profile = profile_factory()
    data = {
        'name': 'Test Gallery Item',
        'resource': file,
    }

    serializer = serializers.GalleryItemSerializer(data=data)
    assert serializer.is_valid()

    item = serializer.save(profile=profile)
    file.seek(0)

    assert item.name == data['name']
    assert item.resource.read().decode('utf8') == file.read()


def test_serialize(api_rf, gallery_item_factory, serializer_context):
    """
    Test serializing a gallery item.
    """
    item = gallery_item_factory()
    serializer = serializers.GalleryItemSerializer(
        item,
        context=serializer_context)

    item_request = api_rf.get(item.get_absolute_url())
    resource_request = api_rf.get(item.resource.url)

    expected = {
        'id': item.id,
        'url': item_request.build_absolute_uri(),
        'name': item.name,
        'resource': resource_request.build_absolute_uri(),
    }

    assert serializer.data == expected


def test_update(gallery_item_factory, serializer_context):
    """
    Saving a bound serializer with additional data should update the
    gallery item bound to the serializer.
    """
    item = gallery_item_factory(name='Old Name')
    data = {
        'name': 'New Name',
    }

    serializer = serializers.GalleryItemSerializer(
        item,
        context=serializer_context,
        data=data,
        partial=True)
    assert serializer.is_valid()

    serializer.save()
    item.refresh_from_db()

    assert item.name == data['name']
