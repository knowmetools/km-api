from unittest import mock

from django.core.exceptions import ValidationError

import pytest

from account import serializers


def test_expired_key(password_reset_factory, settings):
    """
    If the provided key corresponds to a password reset that is expired,
    the serializer should not validate.
    """
    settings.PASSWORD_RESET_EXPIRATION_HOURS = 0

    reset = password_reset_factory()
    data = {
        'key': reset.key,
        'new_password': 'newpassword',
    }

    serializer = serializers.PasswordChangeSerializer(data=data)

    assert not serializer.is_valid()


@pytest.mark.django_db
def test_invalid_key():
    """
    If there is no password reset with the given key, the serializer
    should not be valid.
    """
    data = {
        'key': 'invalidkey',
        'new_password': 'newpassword',
    }

    serializer = serializers.PasswordChangeSerializer(data=data)

    assert not serializer.is_valid()


def test_invalid_new_password(api_rf, user_factory):
    """
    If the user's new password is does not pass Django's password
    validation, the serializer should not be valid.
    """
    user = user_factory(password='oldpassword')
    data = {
        'new_password': 'invalidpassword',
        'old_password': 'oldpassword',
    }

    api_rf.user = user
    request = api_rf.get('/')

    serializer = serializers.PasswordChangeSerializer(
        context={'request': request},
        data=data)

    with mock.patch(
            'account.serializers.password_validation.validate_password',
            side_effect=ValidationError('Invalid password')):
        assert not serializer.is_valid()


def test_invalid_old_password(api_rf, user_factory):
    """
    If the user provides an invalid old password, the serializer should
    not be valid.
    """
    user = user_factory(password='oldpassword')
    data = {
        'new_password': 'newpassword',
        'old_password': 'fakepassword',
    }

    api_rf.user = user
    request = api_rf.get('/')

    serializer = serializers.PasswordChangeSerializer(
        context={'request': request},
        data=data)

    assert not serializer.is_valid()


def test_save(api_rf, user_factory):
    """
    Saving the serializer should update the user's password.
    """
    user = user_factory(password='oldpassword')
    data = {
        'new_password': 'newpassword',
        'old_password': 'oldpassword',
    }

    api_rf.user = user
    request = api_rf.get('/')

    serializer = serializers.PasswordChangeSerializer(
        context={'request': request},
        data=data)
    assert serializer.is_valid()

    with mock.patch.object(
            user,
            'send_password_changed_email') as mock_send_mail:
        serializer.save()

    # Regression test for #35
    user.refresh_from_db()

    assert user.check_password(data['new_password'])
    assert mock_send_mail.call_count == 1


def test_save_with_key(password_reset_factory):
    """
    Providing a password reset key to the serializer should also allow
    the user to change their password.
    """
    reset = password_reset_factory()
    user = reset.user

    data = {
        'key': reset.key,
        'new_password': 'newpassword',
    }

    serializer = serializers.PasswordChangeSerializer(data=data)
    assert serializer.is_valid()

    serializer.save()
    user.refresh_from_db()

    assert user.check_password(data['new_password'])
    assert user.password_resets.count() == 0


def test_validate_duplicate_passwords(api_rf, user_factory):
    """
    Entering a new password that is the same as the existing password
    should cause the serializer to be invalid.
    """
    user = user_factory(password='oldpassword')
    data = {
        'new_password': 'oldpassword',
        'old_password': 'oldpassword',
    }

    api_rf.user = user
    request = api_rf.get('/')

    serializer = serializers.PasswordChangeSerializer(
        context={'request': request},
        data=data)

    assert not serializer.is_valid()
