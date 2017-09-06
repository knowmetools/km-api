from unittest import mock

from know_me import serializers


def test_create(km_user_factory):
    """
    Saving the serializer should use the Know Me user's ``share`` method
    to create a new accessor.
    """
    km_user = km_user_factory()
    data = {
        'can_write': True,
        'email': 'test@example.com',
        'has_private_profile_access': True,
    }

    serializer = serializers.KMUserAccessorSerializer(data=data)
    assert serializer.is_valid()

    with mock.patch.object(km_user, 'share', autospec=True) as mock_share:
        serializer.save(km_user=km_user)

    assert mock_share.call_count == 1
    assert mock_share.call_args[0] == (data['email'],)
    assert mock_share.call_args[1] == {
        'can_write': data['can_write'],
        'has_private_profile_access': data['has_private_profile_access'],
    }


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
        email=user.email,
        km_user=km_user,
        user_with_access=user)

    serializer = serializers.KMUserAccessorSerializer(
        km_user_accessor,
        context=serializer_context)

    km_user_serializer = serializers.KMUserDetailSerializer(
        km_user,
        context=serializer_context)

    expected = {
        'accepted': False,
        'can_write': False,
        'email': km_user_accessor.email,
        'has_private_profile_access': False,
        'km_user': km_user_serializer.data,
    }

    assert serializer.data == expected
