from know_me import serializers


def test_create(user_factory):
    """
    Saving a serializer containing valid data should create a new
    profile.
    """
    user = user_factory()
    data = {
        'name': 'John',
        'quote': "Hi, I'm John",
        'welcome_message': 'This is my profile.',
    }

    serializer = serializers.ProfileListSerializer(data=data)
    assert serializer.is_valid()

    serializer.save(user=user)
    profile = user.profile

    assert profile.name == data['name']
    assert profile.quote == data['quote']
    assert profile.welcome_message == data['welcome_message']
    assert profile.user == user


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
