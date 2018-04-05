from know_me.profile import serializers


def test_serialize(
        api_rf,
        media_resource_category_factory,
        media_resource_factory,
        serialized_time):
    """
    Test serializing a media resource.
    """
    # Note that it is not intended for a resource to have both a file
    # and link defined at the same time. This is enforced by serializer
    # validation. We do it here for testing purposes.
    category = media_resource_category_factory()
    resource = media_resource_factory(
        category=category,
        km_user=category.km_user,
        link='https://example.com')

    api_rf.user = category.km_user.user
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
        'cover_style': resource.cover_style,
        'file': file_request.build_absolute_uri(),
        'link': resource.link,
        'name': resource.name,
        'permissions': {
            'read': category.has_object_read_permission(request),
            'write': category.has_object_write_permission(request),
        },
    }

    assert serializer.data == expected


def test_validate_file(file):
    """
    The serializer should validate when provided a file and name.
    """
    data = {
        'file': file,
        'name': 'Test Resource',
    }
    serializer = serializers.MediaResourceSerializer(data=data)

    assert serializer.is_valid()


def test_validate_link():
    """
    The serializer should validate when provided a link and name.
    """
    data = {
        'link': 'https://example.com',
        'name': 'Test Link Resource',
    }
    serializer = serializers.MediaResourceSerializer(data=data)

    assert serializer.is_valid()


def test_validate_link_and_file(file):
    """
    The serializer should not accept both a file and a link.
    """
    data = {
        'file': file,
        'link': 'https://example.com',
        'name': 'Test File and Link Resource',
    }
    serializer = serializers.MediaResourceSerializer(data=data)

    assert not serializer.is_valid()
    assert set(serializer.errors.keys()) == {'non_field_errors'}


def test_validate_no_link_or_file():
    """
    A serializer without a file or a link should not be valid.
    """
    data = {
        'name': 'Test Empty Resource',
    }
    serializer = serializers.MediaResourceSerializer(data=data)

    assert not serializer.is_valid()
    assert set(serializer.errors.keys()) == {'non_field_errors'}


def test_validate_no_link_or_file_partial_update(media_resource_factory):
    """
    If performing a partial update on a resource, the serializer should
    accept no file or link.
    """
    resource = media_resource_factory(name='Old Name')
    data = {
        'name': 'New Name',
    }
    serializer = serializers.MediaResourceSerializer(
        resource,
        data=data,
        partial=True)

    assert serializer.is_valid()


def test_validate_no_link_or_file_update(media_resource_factory):
    """
    If performing a full update, the serializer should require a file or
    link.
    """
    resource = media_resource_factory(name='Old Name')
    data = {
        'name': 'New Name',
    }
    serializer = serializers.MediaResourceSerializer(resource, data=data)

    assert not serializer.is_valid()
    assert set(serializer.errors.keys()) == {'non_field_errors'}
