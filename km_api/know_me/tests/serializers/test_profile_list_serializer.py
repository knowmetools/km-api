from know_me import serializers


def test_serialize(profile_factory):
    """
    Test serializing a profile.
    """
    profile = profile_factory()
    serializer = serializers.ProfileListSerializer(profile)

    expected = {
        'id': profile.id,
        'name': profile.name,
        'quote': profile.quote,
        'welcome_message': profile.welcome_message,
    }

    assert serializer.data == expected
