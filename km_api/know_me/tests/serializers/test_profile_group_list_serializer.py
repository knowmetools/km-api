from know_me import serializers


def test_create(km_user_factory, serializer_context):
    """
    Saving a serializer instance with valid data should create a new
    profile group.
    """
    km_user = km_user_factory()
    data = {
        'name': 'Profile Group',
        'is_default': True,
    }

    serializer = serializers.ProfileGroupListSerializer(
        context=serializer_context,
        data=data)
    assert serializer.is_valid()

    group = serializer.save(km_user=km_user)

    assert group.name == data['name']
    assert group.km_user == km_user
    assert group.is_default == data['is_default']


def test_serialize(api_rf, profile_group_factory, serializer_context):
    """
    Test serializing a profile group.
    """
    group = profile_group_factory()

    serializer = serializers.ProfileGroupListSerializer(
        group,
        context=serializer_context)

    url_request = api_rf.get(group.get_absolute_url())

    expected = {
        'id': group.id,
        'url': url_request.build_absolute_uri(),
        'name': group.name,
        'is_default': group.is_default,
    }

    assert serializer.data == expected
