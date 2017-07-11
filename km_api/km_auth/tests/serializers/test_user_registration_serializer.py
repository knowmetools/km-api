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

    serializer = serializers.UserRegistrationSerializer(data=data)
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
    serializer = serializers.UserRegistrationSerializer(user)

    expected = {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }

    assert serializer.data == expected
