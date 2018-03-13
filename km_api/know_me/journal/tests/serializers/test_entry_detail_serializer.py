from know_me.journal import serializers


def test_serialize(api_rf, entry_factory):
    """
    Test serializing a journal entry.
    """
    entry = entry_factory()
    api_rf.user = entry.km_user.user
    request = api_rf.get('/')

    serializer = serializers.EntryDetailSerializer(
        entry,
        context={'request': request})
    list_serializer = serializers.EntryListSerializer(
        entry,
        context={'request': request})

    additional = {
        'permissions': {
            'read': entry.has_object_read_permission(request),
            'write': entry.has_object_write_permission(request),
        },
        'text': entry.text,
    }

    expected = dict(list_serializer.data.items())
    expected.update(additional)

    assert serializer.data == expected


def test_validate():
    """
    Test validating the data required to create a comment.
    """
    data = {
        'text': 'My comment text.',
    }
    serializer = serializers.EntryDetailSerializer(data=data)

    assert serializer.is_valid
