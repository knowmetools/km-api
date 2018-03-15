from know_me.journal import serializers


def test_serialize(
        api_rf,
        entry_comment_factory,
        entry_factory,
        image,
        serialized_time):
    """
    Test serializing a journal entry.
    """
    entry = entry_factory(attachment=image)
    request = api_rf.get(entry.get_absolute_url())

    entry_comment_factory(entry=entry)
    entry_comment_factory(entry=entry)

    serializer = serializers.EntryListSerializer(
        entry,
        context={'request': request})

    comments_url = api_rf.get(entry.get_comments_url()).build_absolute_uri()
    attachment_url = api_rf.get(entry.attachment.url).build_absolute_uri()

    expected = {
        'id': entry.id,
        'url': request.build_absolute_uri(),
        'created_at': serialized_time(entry.created_at),
        'updated_at': serialized_time(entry.updated_at),
        'attachment': attachment_url,
        'comment_count': entry.comments.count(),
        'comments_url': comments_url,
        'km_user_id': entry.km_user.id,
        'text': entry.text,
    }

    assert serializer.data == expected
