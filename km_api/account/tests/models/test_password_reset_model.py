from django.utils import timezone

from account import models


def test_create(user_factory):
    """
    Test creating a new password reset.
    """
    reset = models.PasswordReset.objects.create(
        key='key',
        user=user_factory())

    assert reset.created_at <= timezone.now()


def test_string_conversion(password_reset_factory):
    """
    Converting a password reset into a string should return info about
    the password reset.
    """
    reset = password_reset_factory()
    expected = 'Password reset for {user}'.format(user=reset.user)

    assert str(reset) == expected
