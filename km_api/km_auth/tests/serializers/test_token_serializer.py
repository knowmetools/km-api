import pytest

from km_auth import serializers


@pytest.mark.django_db
def test_validate_invalid_credentials():
    """
    If the credentials provided are not valid, the serializer should not
    be valid.
    """
    data = {"email": "test@example.com", "password": "password"}

    serializer = serializers.TokenSerializer(data=data)

    assert not serializer.is_valid()


def test_validate_verified_email(email_factory, user_factory):
    """
    A user with a verified email should be able to obtain a token from
    the serializer.
    """
    user = user_factory(password="password")
    email = email_factory(is_verified=True, user=user)

    data = {"email": email.email, "password": "password"}

    serializer = serializers.TokenSerializer(data=data)

    assert serializer.is_valid()
    assert serializer.validated_data["user"] == user
