from know_me.profile import serializers


def test_serialize(api_rf, profile_topic_factory, serialized_time):
    """
    Test serializing a profile topic.
    """
    topic = profile_topic_factory()

    api_rf.user = topic.profile.km_user.user
    request = api_rf.get(topic.get_absolute_url())

    serializer = serializers.ProfileTopicSerializer(
        topic,
        context={'request': request})

    expected = {
        'id': topic.id,
        'url': request.build_absolute_uri(),
        'created_at': serialized_time(topic.created_at),
        'updated_at': serialized_time(topic.updated_at),
        'is_detailed': topic.is_detailed,
        'name': topic.name,
        'permissions': {
            'read': topic.has_object_read_permission(request),
            'write': topic.has_object_write_permission(request),
        },
        'profile_id': topic.profile.id,
    }

    assert serializer.data == expected


def test_validate():
    """
    Test validating the attributes required to create a new profile
    topic.
    """
    data = {
        'is_detailed': True,
        'name': 'Test Topic',
    }
    serializer = serializers.ProfileTopicSerializer(data=data)

    assert serializer.is_valid()
