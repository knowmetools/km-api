from know_me import serializers


def test_serialize(
        api_rf,
        profile_factory,
        profile_topic_factory,
        serializer_context):
    """
    Test serializing a profile.
    """
    profile = profile_factory()
    profile_topic_factory(profile=profile)
    profile_topic_factory(profile=profile)

    serializer = serializers.ProfileDetailSerializer(
        profile,
        context=serializer_context)
    topic_serializer = serializers.ProfileTopicSerializer(
        profile.topics,
        context=serializer_context,
        many=True)

    url_request = api_rf.get(profile.get_absolute_url())
    topic_list_request = api_rf.get(profile.get_topic_list_url())

    expected = {
        'id': profile.id,
        'url': url_request.build_absolute_uri(),
        'name': profile.name,
        'topics_url': topic_list_request.build_absolute_uri(),
        'topics': topic_serializer.data,
        'permissions': {
            'read': profile.has_object_read_permission(topic_list_request),
            'write': profile.has_object_write_permission(topic_list_request),
        }
    }

    assert serializer.data == expected


def test_update(profile_factory):
    """
    Saving a bound serializer with valid data should update the profile
    bound to the serializer.
    """
    profile = profile_factory(name='Old Profile')
    data = {
        'name': 'New Profile',
    }

    serializer = serializers.ProfileDetailSerializer(
        profile,
        data=data,
        partial=True)
    assert serializer.is_valid()

    serializer.save()
    profile.refresh_from_db()

    assert profile.name == data['name']
