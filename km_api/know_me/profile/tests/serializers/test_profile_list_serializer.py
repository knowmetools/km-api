from know_me.profile import serializers


def test_serialize_profile(api_rf, profile_factory, serialized_time):
    """
    Test serializing a profile.
    """
    profile = profile_factory()

    api_rf.user = profile.km_user.user
    request = api_rf.get(profile.get_absolute_url())

    serializer = serializers.ProfileListSerializer(
        profile,
        context={'request': request})

    topics_url = api_rf.get(profile.get_topic_list_url()).build_absolute_uri()

    expected = {
        'id': profile.id,
        'url': request.build_absolute_uri(),
        'created_at': serialized_time(profile.created_at),
        'updated_at': serialized_time(profile.updated_at),
        'name': profile.name,
        'permissions': {
            'read': profile.has_object_read_permission(request),
            'write': profile.has_object_write_permission(request),
        },
        'topics_url': topics_url,
    }

    assert serializer.data == expected
