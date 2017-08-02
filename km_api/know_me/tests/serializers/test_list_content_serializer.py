from know_me import serializers


def test_create(profile_item_factory):
    """
    Saving a serializer with valid data should create a new list content
    instance.
    """
    item = profile_item_factory()
    data = {}

    serializer = serializers.ListContentSerializer(data=data)
    assert serializer.is_valid()

    content = serializer.save(profile_item=item)

    assert content.profile_item == item


def test_serialize(list_content_factory, list_entry_factory):
    """
    Test serializing list content.
    """
    content = list_content_factory()
    list_entry_factory(list_content=content)
    list_entry_factory(list_content=content)

    serializer = serializers.ListContentSerializer(content)

    entry_serializer = serializers.ListEntrySerializer(
        content.entries.all(),
        many=True)

    expected = {
        'id': content.id,
        'entries': entry_serializer.data,
    }

    assert serializer.data == expected
