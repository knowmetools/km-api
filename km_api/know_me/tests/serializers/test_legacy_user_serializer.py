from know_me import serializers


def test_serialize(api_rf, legacy_user_factory, serialized_time):
    """
    Test serializing a legacy user.
    """
    user = legacy_user_factory()
    request = api_rf.get(user.get_absolute_url())

    serializer = serializers.LegacyUserSerializer(
        user, context={"request": request}
    )

    expected = {
        "id": user.id,
        "url": request.build_absolute_uri(),
        "created_at": serialized_time(user.created_at),
        "updated_at": serialized_time(user.updated_at),
        "email": user.email,
    }

    assert serializer.data == expected
