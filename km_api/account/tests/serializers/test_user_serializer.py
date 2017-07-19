from account import serializers


def test_serialize(user_factory):
    """
    Test serializing a user.
    """
    user = user_factory()
    serializer = serializers.UserSerializer(user)

    expected = {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }

    assert serializer.data == expected


def test_update(user_factory):
    """
    Saving a serializer with additional data should update the user
    instance the serializer is bound to.
    """
    user = user_factory(first_name='Bob')
    data = {
        'first_name': 'John',
    }

    serializer = serializers.UserSerializer(user, data=data, partial=True)
    assert serializer.is_valid()

    serializer.save()
    user.refresh_from_db()

    assert user.first_name == data['first_name']
