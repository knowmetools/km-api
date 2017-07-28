from know_me import serializers


def test_create(file, profile_factory):
    """
    Saving a serializer containing valid data should create a new
    media resource attached to the given profile.
    """
    profile = profile_factory()
    data = {
        'name': 'Test Media Resource',
        'file': file,
    }

    serializer = serializers.MediaResourceSerializer(data=data)
    assert serializer.is_valid()

    resource = serializer.save(profile=profile)
    file.seek(0)

    assert resource.name == data['name']
    assert resource.file.read() == file.read()


def test_serialize(api_rf, media_resource_factory, serializer_context):
    """
    Test serializing a media resource.
    """
    resource = media_resource_factory()
    serializer = serializers.MediaResourceSerializer(
        resource,
        context=serializer_context)

    resource_request = api_rf.get(resource.get_absolute_url())
    file_request = api_rf.get(resource.file.url)

    expected = {
        'id': resource.id,
        'url': resource_request.build_absolute_uri(),
        'name': resource.name,
        'file': file_request.build_absolute_uri(),
    }

    assert serializer.data == expected


def test_update(media_resource_factory, serializer_context):
    """
    Saving a bound serializer with additional data should update the
    media resource bound to the serializer.
    """
    resource = media_resource_factory(name='Old Name')
    data = {
        'name': 'New Name',
    }

    serializer = serializers.MediaResourceSerializer(
        resource,
        context=serializer_context,
        data=data,
        partial=True)
    assert serializer.is_valid()

    serializer.save()
    resource.refresh_from_db()

    assert resource.name == data['name']
