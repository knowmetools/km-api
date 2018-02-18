from know_me.profile import serializers


def test_serialize_profile(api_rf, profile_factory, serialized_time):
    """
    Test serializing a profile.
    """
    profile = profile_factory()
    request = api_rf.get(profile.get_absolute_url())

    serializer = serializers.ProfileListSerializer(
        profile,
        context={'request': request})

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
    }

    assert serializer.data == expected
