from unittest import mock

import pytest

from account.models import EmailConfirmation
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

    with mock.patch(
            'km_auth.serializers.EmailConfirmation.send_confirmation',
            autospec=True) as mock_confirm:
        user = serializer.save()

    assert user.email == data['email']
    assert user.first_name == data['first_name']
    assert user.last_name == data['last_name']
    assert user.check_password(data['password'])

    # Ensure we sent the user an email confirmation
    assert EmailConfirmation.objects.count() == 1
    assert mock_confirm.call_count == 1


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
