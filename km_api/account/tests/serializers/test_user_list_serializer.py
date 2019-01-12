from account import serializers


def test_serialize(serialized_time, user_factory):
    """
    Test serializing a user.
    """
    user = user_factory()
    serializer = serializers.UserListSerializer(user)

    expected = {
        "id": user.id,
        "created_at": serialized_time(user.created_at),
        "updated_at": serialized_time(user.updated_at),
        "first_name": user.first_name,
        "is_active": user.is_active,
        "is_staff": user.is_staff,
        "last_name": user.last_name,
        "primary_email": user.primary_email.email,
    }

    assert serializer.data == expected
