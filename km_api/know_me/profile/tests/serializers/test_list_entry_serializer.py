from know_me.profile import serializers


def test_serialize(api_rf, list_entry_factory, serialized_time):
    """
    Test serializing a list entry.
    """
    entry = list_entry_factory()

    api_rf.user = entry.profile_item.topic.profile.km_user.user
    request = api_rf.get(entry.get_absolute_url())

    serializer = serializers.ListEntrySerializer(
        entry,
        context={'request': request})

    expected = {
        'id': entry.id,
        'created_at': serialized_time(entry.created_at),
        'updated_at': serialized_time(entry.updated_at),
        'permissions': {
            'read': entry.has_object_read_permission(request),
            'write': entry.has_object_write_permission(request),
        },
        'profile_item_id': entry.profile_item.id,
        'text': entry.text,
    }

    assert serializer.data == expected


def test_validate():
    """
    Test validating the data used to create a new list entry.
    """
    data = {
        'text': 'Test List Entry',
    }
    serializer = serializers.ListEntrySerializer(data=data)

    assert serializer.is_valid()
