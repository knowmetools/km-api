from account import serializers


def test_serialize(api_rf, image, user_factory):
    """
    Test serializing a user.
    """
    user = user_factory(image=image)
    request = api_rf.get(user.image.url)

    serializer = serializers.UserInfoSerializer(
        user,
        context={'request': request})

    expected = {
        'first_name': user.first_name,
        'image': request.build_absolute_uri(),
        'last_name': user.last_name,
    }

    assert serializer.data == expected
