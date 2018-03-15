from account.serializers import UserInfoSerializer
from know_me.journal import serializers


def test_serialize(api_rf, entry_comment_factory, serialized_time):
    """
    Test serializing an entry comment.
    """
    comment = entry_comment_factory()
    api_rf.user = comment.user
    request = api_rf.get(comment.get_absolute_url())

    serializer = serializers.EntryCommentSerializer(
        comment,
        context={'request': request})
    user_serializer = UserInfoSerializer(
        comment.user,
        context={'request': request})

    expected = {
        'id': comment.id,
        'url': request.build_absolute_uri(),
        'created_at': serialized_time(comment.created_at),
        'updated_at': serialized_time(comment.updated_at),
        'permissions': {
            'destroy': comment.has_object_destroy_permission(request),
            'read': comment.has_object_read_permission(request),
            'write': comment.has_object_write_permission(request),
        },
        'text': comment.text,
        'user': user_serializer.data,
    }

    assert serializer.data == expected


def test_validate():
    """
    Test validating the content required to create a new comment.
    """
    data = {
        'text': 'My sample comment text.',
    }
    serializer = serializers.EntryCommentSerializer(data=data)

    assert serializer.is_valid()
