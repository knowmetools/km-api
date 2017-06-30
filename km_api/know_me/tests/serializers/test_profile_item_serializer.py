from know_me import serializers


def test_create(profile_row_factory):
    """
    Saving a serializer with valid data should create a new profile
    item.
    """
    row = profile_row_factory()
    data = {
        'name': 'My Profile Item',
        'text': 'Some sample text.',
    }

    serializer = serializers.ProfileItemSerializer(data=data)
    assert serializer.is_valid()

    item = serializer.save(row=row)

    assert item.name == data['name']
    assert item.text == data['text']
    assert item.row == row


def test_serialize(profile_item_factory):
    """
    Test serializing a profile item.
    """
    item = profile_item_factory()
    serializer = serializers.ProfileItemSerializer(item)

    expected = {
        'id': item.id,
        'name': item.name,
        'text': item.text,
    }

    assert serializer.data == expected


def test_update(profile_item_factory):
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
        data=data,
        partial=True)
    assert serializer.is_valid()

    serializer.save()
    item.refresh_from_db()

    assert item.name == data['name']
