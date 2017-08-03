from know_me import serializers


def test_create(list_content_factory):
    """
    Saving a serializer with valid data should create a new list entry.
    """
    list_content = list_content_factory()
    data = {
        'text': 'Test list entry.',
    }

    serializer = serializers.ListEntrySerializer(data=data)
    assert serializer.is_valid()

    entry = serializer.save(list_content=list_content)

    assert entry.list_content == list_content
    assert entry.text == data['text']


def test_serialize(list_entry_factory):
    """
    Test serializing a list entry.
    """
    entry = list_entry_factory()
    serializer = serializers.ListEntrySerializer(entry)

    expected = {
        'id': entry.id,
        'text': entry.text,
    }

    assert serializer.data == expected


def test_update(list_entry_factory):
    """
    Saving a bound serializer should update the list entry the
    serializer is bound to with the provided data.
    """
    entry = list_entry_factory(text='Old text.')
    data = {
        'text': 'New text.',
    }

    serializer = serializers.ListEntrySerializer(
        entry,
        data=data)
    assert serializer.is_valid()

    serializer.save()
    entry.refresh_from_db()

    assert entry.text == data['text']
