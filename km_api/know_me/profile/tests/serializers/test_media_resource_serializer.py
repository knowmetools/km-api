from know_me.profile import serializers


def test_serialize(
        api_rf,
        media_resource_category_factory,
        media_resource_factory,
        serialized_time):
    """
    Test serializing a media resource.
    """
    category = media_resource_category_factory()
    resource = media_resource_factory(
        category=category,
        km_user=category.km_user)
    request = api_rf.get(resource.get_absolute_url())

    serializer = serializers.MediaResourceSerializer(
        resource,
        context={'request': request})

    file_request = api_rf.get(resource.file.url)

    expected = {
        'id': resource.id,
        'url': request.build_absolute_uri(),
        'created_at': serialized_time(resource.created_at),
        'updated_at': serialized_time(resource.updated_at),
        'category_id': resource.category.id,
        'file': file_request.build_absolute_uri(),
        'name': resource.name,
        'permissions': {
            'read': category.has_object_read_permission(request),
            'write': category.has_object_write_permission(request),
        },
    }

    assert serializer.data == expected


def test_validate(file):
    """
    The serializer should validate when provided the minimum amount of
    information.
    """
    data = {
        'file': file,
        'name': 'Test Resource',
    }
    serializer = serializers.MediaResourceSerializer(data=data)

    assert serializer.is_valid()
