from know_me.journal import serializers


def test_serialize(api_rf, entry_comment_factory, entry_factory):
    """
    Test serializing a journal entry.
    """
    entry = entry_factory()
    api_rf.user = entry.km_user.user
    request = api_rf.get(entry.get_absolute_url())

    entry_comment_factory(entry=entry)
    entry_comment_factory(entry=entry)

    serializer = serializers.EntryDetailSerializer(
        entry,
        context={'request': request})
    comment_serializer = serializers.EntryCommentSerializer(
        entry.comments.all(),
        context={'request': request},
        many=True)
    list_serializer = serializers.EntryListSerializer(
        entry,
        context={'request': request})

    additional = {
        'comments': comment_serializer.data,
        'permissions': {
            'read': entry.has_object_read_permission(request),
            'write': entry.has_object_write_permission(request),
        },
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
