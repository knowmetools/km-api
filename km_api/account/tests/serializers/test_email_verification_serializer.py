import pytest

from account import models, serializers


def test_save_valid_key(email_confirmation_factory, user_factory):
    """
    If a serializer with a valid key is saved, the email that the
    confirmation points to should be verified, and the confirmation
    should be deleted.
    """
    user = user_factory(password='password')
    confirmation = email_confirmation_factory(user=user)

    data = {
        'key': confirmation.key,
        'password': 'password',
    }

    serializer = serializers.EmailVerificationSerializer(data=data)
    assert serializer.is_valid()

    serializer.save()
    user.refresh_from_db()

    assert models.EmailConfirmation.objects.count() == 0
    assert user.email_verified


def test_validate_expired(email_confirmation_factory, settings, user_factory):
    """
    If a key is given for an expired confirmation, the serializer should
    not be valid.
    """
    settings.EMAIL_CONFIRMATION_EXPIRATION_DAYS = 0

    user = user_factory(password='password')
    confirmation = email_confirmation_factory(user=user)
    data = {
        'key': confirmation.key,
        'password': 'password',
    }

    serializer = serializers.EmailVerificationSerializer(data=data)

    assert not serializer.is_valid()


def test_validate_inactive_user(email_confirmation_factory, user_factory):
    """
    Inactive users should not be able to confirm an email address.
    """
    user = user_factory(is_active=False, password='password')
    confirmation = email_confirmation_factory(user=user)

    data = {
        'key': confirmation.key,
        'password': 'password',
    }

    serializer = serializers.EmailVerificationSerializer(data=data)

    assert not serializer.is_valid()


def test_validate_invalid_password(email_confirmation_factory, user_factory):
    """
    If the password given does not match the password of the user
    associated with the confirmation, the serializer should not be
    valid.
    """
    user = user_factory(password='password')
    confirmation = email_confirmation_factory(user=user)

    data = {
        'key': confirmation.key,
        'password': 'notpassword',
    }

    serializer = serializers.EmailVerificationSerializer(data=data)

    assert not serializer.is_valid()


@pytest.mark.django_db
def test_validate_unknown_key():
    """
    If the key given to the serializer has no corresponding email
    confirmation, the serializer should not be valid.
    """
    data = {
        'key': 'randomkey',
    }

    serializer = serializers.EmailVerificationSerializer(data=data)

    assert not serializer.is_valid()
