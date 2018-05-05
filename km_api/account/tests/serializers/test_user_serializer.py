from account import serializers


def test_serialize(api_rf, image, serialized_time, user_factory):
    """
    Test serializing a user.
    """
    user = user_factory(image=image)
    request = api_rf.get(user.image.url)

    serializer = serializers.UserSerializer(user, context={'request': request})

    expected = {
        'id': user.id,
        'created_at': serialized_time(user.created_at),
        'updated_at': serialized_time(user.updated_at),
        'first_name': user.first_name,
        'image': request.build_absolute_uri(),
        'is_staff': user.is_staff,
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
