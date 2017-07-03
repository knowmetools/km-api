from know_me import serializers


def test_create(profile_row_factory, serializer_context):
    """
    Saving a serializer with valid data should create a new profile
    item.
    """
    row = profile_row_factory()
    data = {
        'name': 'My Profile Item',
        'text': 'Some sample text.',
    }

    serializer = serializers.ProfileItemSerializer(
        context=serializer_context,
        data=data)
    assert serializer.is_valid()

    item = serializer.save(row=row)

    assert item.name == data['name']
    assert item.text == data['text']
    assert item.row == row


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
        'text': item.text,
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
