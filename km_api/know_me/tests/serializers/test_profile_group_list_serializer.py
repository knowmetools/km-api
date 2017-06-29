from know_me import serializers


def test_create(profile_factory):
    """
    Saving a serializer instance with valid data should create a new
    profile group.
    """
    profile = profile_factory()
    data = {
        'name': 'Profile Group',
        'profile': profile.id,
        'is_default': True,
    }

    serializer = serializers.ProfileGroupListSerializer(data=data)
    assert serializer.is_valid()

    group = serializer.save()

    assert group.name == data['name']
    assert group.profile == profile
    assert group.is_default == data['is_default']


def test_serialize(profile_group_factory):
    """
    Test serializing a profile group.
    """
    group = profile_group_factory()
    serializer = serializers.ProfileGroupListSerializer(group)

    expected = {
        'id': group.id,
        'name': group.name,
        'profile': group.profile.id,
        'is_default': group.is_default,
    }

    assert serializer.data == expected
