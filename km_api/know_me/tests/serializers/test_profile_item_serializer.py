from know_me import serializers


def test_create(profile_topic_factory, serializer_context):
    """
    Saving a serializer with valid data should create a new profile
    item.
    """
    topic = profile_topic_factory()

    serializer_context['profile'] = topic.group.profile

    data = {
        'name': 'My Profile Item',
    }

    serializer = serializers.ProfileItemSerializer(
        context=serializer_context,
        data=data)
    assert serializer.is_valid(), serializer.errors

    item = serializer.save(topic=topic)

    assert item.name == data['name']
    assert item.topic == topic


def test_serialize(api_rf, profile_item_factory, serializer_context):
    """
    Test serializing a profile item.
    """
    item = profile_item_factory()

    serializer = serializers.ProfileItemSerializer(
        item,
        context=serializer_context)

    url_request = api_rf.get(item.get_absolute_url())

    expected = {
        'id': item.id,
        'url': url_request.build_absolute_uri(),
        'name': item.name,
    }

    assert serializer.data == expected


def test_update(profile_item_factory, serializer_context):
    """
    Saving a bound serializer with additional data should update the
    profile item bound to the serializer.
    """
    item = profile_item_factory(name='Old Name')
    data = {
        'name': 'New Name',
    }

    serializer = serializers.ProfileItemSerializer(
        item,
        context=serializer_context,
        data=data,
        partial=True)
    assert serializer.is_valid()

    serializer.save()
    item.refresh_from_db()

    assert item.name == data['name']
