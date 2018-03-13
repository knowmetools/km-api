from account import serializers


def test_serialize(user_factory):
    """
    Test serializing a user.
    """
    user = user_factory()
    serializer = serializers.UserInfoSerializer(user)

    expected = {
        'first_name': user.first_name,
        'last_name': user.last_name,
    }

    assert serializer.data == expected
