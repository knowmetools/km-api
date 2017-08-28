from know_me import serializers


def test_serialize(
        api_rf,
        km_user_factory,
        km_user_accessor_factory,
        serializer_context,
        user_factory):
    """
    Test serializing a km_user_accessor.
    """
    km_user = km_user_factory()
    user = user_factory()
    km_user_accessor = km_user_accessor_factory(
        km_user=km_user,
        user_with_access=user)

    serializer = serializers.KMUserAccessorSerializer(
        km_user_accessor,
        context=serializer_context)

    expected = {
        'accepted': False,
        'can_write': False,
        'has_private_profile_access': False,
        'km_user': km_user,
        'user_with_access_email': user.email,
    }

    assert serializer.data == expected
