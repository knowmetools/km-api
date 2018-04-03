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

    data = {'is_accepted': True}

    serializer = serializers.KMUserAccessorSerializer(
        accessor,
        context={'request': request},
        data=data,
        partial=True)
    assert serializer.is_valid()

    serializer.save()
    accessor.refresh_from_db()

    assert accessor.is_accepted


def test_accept_by_unauthorized_user(api_rf, km_user_accessor_factory):
    """
    Any user other than the user granted access by the accessor should
    not be able to accept the accessor.
    """
    accessor = km_user_accessor_factory()

    api_rf.user = accessor.km_user.user
    request = api_rf.get('/')

    data = {'is_accepted': True}

    serializer = serializers.KMUserAccessorSerializer(
        accessor,
        context={'request': request},
        data=data,
        partial=True)

    assert not serializer.is_valid()
    assert set(serializer.errors.keys()) == {'is_accepted'}


def test_accept_on_create(db):
    """
    Attempt to create an accessor with ``is_accepted == True`` should
    fail.
    """
    data = {
        'email': 'test@example.com',
        'is_accepted': True,
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
        'email': 'test@example.com',
        'is_admin': True,
    }

    serializer = serializers.KMUserAccessorSerializer(data=data)
    assert serializer.is_valid()

    with mock.patch.object(km_user, 'share', autospec=True) as mock_share:
        serializer.save(km_user=km_user)

    assert mock_share.call_count == 1
    assert mock_share.call_args[0] == (data['email'],)
    assert mock_share.call_args[1] == {'is_admin': data['is_admin']}


def test_serialize(
        api_rf,
        km_user_factory,
        km_user_accessor_factory,
        serialized_time,
        user_factory):
    """
    Test serializing a km_user_accessor.
    """
    km_user = km_user_factory()
    user = user_factory()
    accessor = km_user_accessor_factory(
        email=user.primary_email.email,
        km_user=km_user,
        user_with_access=user)

    api_rf.user = user
    request = api_rf.get(accessor.get_absolute_url())

    serializer = serializers.KMUserAccessorSerializer(
        accessor,
        context={'request': request})

    km_user_serializer = serializers.KMUserListSerializer(
        km_user,
        context={'request': request})

    url = request.build_absolute_uri()

    expected = {
        'id': accessor.id,
        'url': url,
        'created_at': serialized_time(accessor.created_at),
        'updated_at': serialized_time(accessor.updated_at),
        'email': accessor.email,
        'is_accepted': accessor.is_accepted,
        'is_admin': accessor.is_admin,
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
