from know_me import serializers


def test_create(serializer_context, user_factory):
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

    serializer = serializers.ProfileListSerializer(
        context=serializer_context,
        data=data)
    assert serializer.is_valid()

    serializer.save(user=user)
    profile = user.profile

    assert profile.name == data['name']
    assert profile.quote == data['quote']
    assert profile.welcome_message == data['welcome_message']
    assert profile.user == user


def test_serialize(api_rf, profile_factory, serializer_context):
    """
    Test serializing a profile.
    """
    profile = profile_factory()
    serializer = serializers.ProfileListSerializer(
        profile,
        context=serializer_context)

    url_request = api_rf.get(profile.get_absolute_url())

    expected = {
        'id': profile.id,
        'url': url_request.build_absolute_uri(),
        'name': profile.name,
        'quote': profile.quote,
        'welcome_message': profile.welcome_message,
    }

    assert serializer.data == expected
