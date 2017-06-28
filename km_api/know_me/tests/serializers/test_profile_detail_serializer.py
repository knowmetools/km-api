from know_me import serializers


def test_serialize(profile_factory):
    """
    Test serializing a profile.
    """
    profile = profile_factory()
    serializer = serializers.ProfileDetailSerializer(profile)

    expected = {
        'id': profile.id,
        'name': profile.name,
        'quote': profile.quote,
        'welcome_message': profile.welcome_message,
    }

    assert serializer.data == expected


def test_update(profile_factory):
    """
    Saving a bound serializer with valid data should update the profile
    the serializer is bound to.
    """
    profile = profile_factory(name='Jim')
    data = {
        'name': 'John',
    }

    serializer = serializers.ProfileDetailSerializer(
        profile,
        data=data,
        partial=True)
    assert serializer.is_valid()

    serializer.save()
    profile.refresh_from_db()

    assert profile.name == data['name']
