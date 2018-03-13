from know_me.journal import serializers


def test_serialize(api_rf, entry_factory, serialized_time):
    """
    Test serializing a journal entry.
    """
    entry = entry_factory()
    request = api_rf.get('/')

    serializer = serializers.EntryListSerializer(
        entry,
        context={'request': request})

    expected = {
        'id': entry.id,
        'created_at': serialized_time(entry.created_at),
        'updated_at': serialized_time(entry.updated_at),
        'km_user_id': entry.km_user.id,
    }

    assert serializer.data == expected
