import pytest

from km_auth import serializers


@pytest.mark.django_db
def test_create():
    """
    Saving a serializer with valid data should create a new user.
    """
    data = {
        'email': 'test@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'password': 'p455w0rd',
    }

    serializer = serializers.UserDetailSerializer(data=data)
    assert serializer.is_valid()

    user = serializer.save()

    assert user.email == data['email']
    assert user.first_name == data['first_name']
    assert user.last_name == data['last_name']
    assert user.check_password(data['password'])


def test_serialize(user_factory):
    """
    Test serializing a user.
    """
    user = user_factory()
    serializer = serializers.UserDetailSerializer(user)

    expected = {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }

    assert serializer.data == expected


def test_update(user_factory):
    """
    Saving a bound serializer with additional data should update the
    user the serializer is bound to.
    """
    user = user_factory(first_name='John')
    data = {
        'first_name': 'Joe',
    }

    serializer = serializers.UserDetailSerializer(
        user,
        data=data,
        partial=True)
    assert serializer.is_valid()

    serializer.save()
    user.refresh_from_db()

    assert user.first_name == data['first_name']


def test_update_password(user_factory):
    """
    If a new password is included in the data, it should be set as the
    user's new password.
    """
    user = user_factory(password='oldpassword')
    data = {
        'password': 'newp455w0rd',
    }

    serializer = serializers.UserDetailSerializer(
        user,
        data=data,
        partial=True)
    assert serializer.is_valid()

    serializer.save()
    user.refresh_from_db()

    assert user.check_password(data['password'])
