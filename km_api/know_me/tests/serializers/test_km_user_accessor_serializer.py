from unittest import mock

from know_me import serializers


def test_accept(
        api_rf,
        km_user_accessor_factory,
        user_factory):
    """
    The user who is invited through the accessor should be able to mark
    the accessor as accepted.
    """
    user = user_factory()
    accessor = km_user_accessor_factory(user_with_access=user)

    api_rf.user = user
    request = api_rf.get('/')

    data = {'accepted': True}

    serializer = serializers.KMUserAccessorSerializer(
        accessor,
        context={'request': request},
        data=data)
    assert serializer.is_valid()

    serializer.save()
    accessor.refresh_from_db()

    assert accessor.accepted


def test_accept_by_unauthorized_user(api_rf, km_user_accessor_factory):
    """
    Any user other than the user granted access by the accessor should
    not be able to accept the accessor.
    """
    accessor = km_user_accessor_factory()

    api_rf.user = accessor.km_user.user
    request = api_rf.get('/')

    data = {'accepted': True}

    serializer = serializers.KMUserAccessorSerializer(
        accessor,
        context={'request': request},
        data=data)

    assert not serializer.is_valid()
    assert set(serializer.errors.keys()) == {'accepted'}


def test_accept_on_create(db):
    """
    Attempt to create an accessor with ``accepted == True`` should fail.
    """
    data = {
        'accepted': True,
        'email': 'test@example.com',
    }

    serializer = serializers.KMUserAccessorSerializer(data=data)
    assert not serializer.is_valid()


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

    url = km_user_accessor.get_absolute_url(serializer_context['request'])

    expected = {
        'url': url,
        'accepted': False,
        'can_write': False,
        'email': km_user_accessor.email,
        'has_private_profile_access': False,
        'km_user': km_user_serializer.data,
    }

    assert serializer.data == expected


def test_validate_new_email(km_user_accessor_factory):
    """
    Trying to set a new email on an existing accessor should cause the
    serializer to be invalid.
    """
    accessor = km_user_accessor_factory(email='old@example.com')
    data = {
        'email': 'new@example.com',
    }

    serializer = serializers.KMUserAccessorSerializer(accessor, data=data)

    assert not serializer.is_valid()
    assert set(serializer.errors.keys()) == {'email'}
