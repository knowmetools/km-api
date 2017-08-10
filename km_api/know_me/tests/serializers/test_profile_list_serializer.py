from know_me import serializers


def test_create(km_user_factory, serializer_context):
    """
    Saving a serializer instance with valid data should create a new
    profile group.
    """
    km_user = km_user_factory()
    data = {
        'name': 'Profile',
        'is_default': True,
    }

    serializer = serializers.ProfileListSerializer(
        context=serializer_context,
        data=data)
    assert serializer.is_valid()

    profile = serializer.save(km_user=km_user)

    assert profile.name == data['name']
    assert profile.km_user == km_user
    assert profile.is_default == data['is_default']


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
        'is_default': profile.is_default,
    }

    assert serializer.data == expected
