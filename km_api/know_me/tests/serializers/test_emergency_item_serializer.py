from know_me import serializers


def test_create(km_user_factory, media_resource_factory):
    """
    Saving a serializer with valid data should create a new emergency
    item.
    """
    km_user = km_user_factory()
    media_resource = media_resource_factory(km_user=km_user)

    data = {
        'name': 'Test Emergency Item',
        'description': 'Test emergency item description.',
        'media_resource': media_resource.id,
    }

    serializer = serializers.EmergencyItemSerializer(data=data)
    assert serializer.is_valid()

    item = serializer.save(km_user=km_user)

    assert item.name == data['name']
    assert item.description == data['description']
    assert item.media_resource == media_resource

    assert item.km_user == km_user


def test_serialize(
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

    expected = {
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'media_resource': media_resource_serializer.data,
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
