from unittest import mock

from django.core.exceptions import ValidationError

from account import serializers


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

    assert user.check_password(data['new_password'])
    assert mock_send_mail.call_count == 1


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
