from know_me import serializers


def test_create(km_user_factory, media_resource_factory, serializer_context):
    """
    Saving a serializer with valid data should create a new emergency
    item.
    """
    km_user = km_user_factory()
    serializer_context['km_user'] = km_user
    serializer_request = serializer_context['request']

    media_resource = media_resource_factory(km_user=km_user)
    has_read = media_resource.has_object_read_permission(serializer_request)
    has_write = media_resource.has_object_write_permission(serializer_request)

    data = {
        'name': 'Test Emergency Item',
        'description': 'Test emergency item description.',
        'media_resource': media_resource.id,
        'permissions': {
            'read': has_read,
            'write': has_write,
        }
    }

    serializer = serializers.EmergencyItemSerializer(
        context=serializer_context,
        data=data)
    assert serializer.is_valid()

    item = serializer.save(km_user=km_user)

    assert item.name == data['name']
    assert item.description == data['description']
    assert item.media_resource == media_resource

    assert item.km_user == km_user


def test_serialize(
        api_rf,
        emergency_item_factory,
        media_resource_factory,
        serializer_context):
    """
    Test serializing an emergency item.
    """
    media_resource = media_resource_factory()
    item = emergency_item_factory(media_resource=media_resource)

    serializer = serializers.EmergencyItemSerializer(
        item,
        context=serializer_context)

    media_resource_serializer = serializers.MediaResourceSerializer(
        media_resource,
        context=serializer_context)

    url_request = api_rf.get(item.get_absolute_url())
    serializer_request = serializer_context['request']
    has_read = media_resource.has_object_read_permission(serializer_request)
    has_write = media_resource.has_object_write_permission(serializer_request)

    expected = {
        'id': item.id,
        'url': url_request.build_absolute_uri(),
        'name': item.name,
        'description': item.description,
        'media_resource': media_resource_serializer.data,
        'permissions': {
            'read': has_read,
            'write': has_write,
        }
    }

    assert serializer.data == expected


def test_update(emergency_item_factory):
    """
    Saving a serializer bound to an emergency item should update that
    item's information.
    """
    item = emergency_item_factory(name='Old Name')
    data = {
        'name': 'New Name',
    }

    serializer = serializers.EmergencyItemSerializer(
        item,
        data=data,
        partial=True)
    assert serializer.is_valid()

    serializer.save()
    item.refresh_from_db()

    assert item.name == data['name']
