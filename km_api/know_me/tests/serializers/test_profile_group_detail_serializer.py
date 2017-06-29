from know_me import serializers


def test_serialize(profile_group_factory):
    """
    Test serializing a profile group.
    """
    group = profile_group_factory()
    serializer = serializers.ProfileGroupDetailSerializer(group)

    expected = {
        'id': group.id,
        'name': group.name,
        'profile': group.profile.id,
        'is_default': group.is_default,
    }

    assert serializer.data == expected


def test_update(profile_group_factory):
    """
    Saving a bound serializer with valid data should update the profile
    group bound to the serializer.
    """
    group = profile_group_factory(name='Old Group')
    data = {
        'name': 'New Group',
    }

    serializer = serializers.ProfileGroupDetailSerializer(
        group,
        data=data,
        partial=True)
    assert serializer.is_valid()

    serializer.save()
    group.refresh_from_db()

    assert group.name == data['name']
