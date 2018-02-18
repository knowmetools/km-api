from know_me.profile import serializers


def test_serialize_profile(api_rf, profile_factory, profile_topic_factory):
    """
    Test serializing a profile.
    """
    profile = profile_factory()
    request = api_rf.get('/')

    profile_topic_factory(profile=profile)

    serializer = serializers.ProfileDetailSerializer(
        profile,
        context={'request': request})
    list_serializer = serializers.ProfileListSerializer(
        profile,
        context={'request': request})
    topic_serializer = serializers.ProfileTopicSerializer(
        profile.topics,
        context={'request': request},
        many=True)

    topics_url = api_rf.get(profile.get_topic_list_url()).build_absolute_uri()

    additional = {
        'topics': topic_serializer.data,
        'topics_url': topics_url,
    }

    expected = dict(list_serializer.data.items())
    expected.update(additional)

    assert serializer.data == expected
