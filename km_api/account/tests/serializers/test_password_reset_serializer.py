from account import serializers


def test_save_password_reset_serializer(email_factory):
    """
    Saving a password reset serializer with a verified email address
    should create a new password reset for that email.
    """
    email = email_factory(verified=True)
    user = email.user

    data = {
        'email': email.email,
    }

    serializer = serializers.PasswordResetSerializer(data=data)
    assert serializer.is_valid()

    serializer.save()

    assert user.password_resets.count() == 1
