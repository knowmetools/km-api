from unittest import mock

from account import serializers


def test_save_password_reset_serializer(email_factory):
    """
    Saving a password reset serializer with a verified email address
    should create a new password reset for that email.
    """
    email = email_factory(verified=True)

    data = {
        'email': email.email,
    }

    serializer = serializers.PasswordResetSerializer(data=data)
    assert serializer.is_valid()

    with mock.patch(
            'account.models.PasswordReset.create_and_send') as mock_send:
        serializer.save()

    assert mock_send.call_count == 1
    assert mock_send.call_args[0] == (email.email,)
