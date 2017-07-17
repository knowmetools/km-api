from django.core import mail
from django.template.loader import render_to_string
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


def test_create_and_send(email_factory, settings):
    """
    If the provided email address has been verified, a password reset
    should be created and sent to the provided address.
    """
    settings.PASSWORD_RESET_LINK_TEMPLATE = 'example.com/reset/?key={key}'

    email = email_factory(verified=True)

    reset = models.PasswordReset.create_and_send(email.email)

    expected_link = settings.PASSWORD_RESET_LINK_TEMPLATE.format(
        key=reset.key)
    expected_content = render_to_string(
        'account/email/reset-password.txt',
        {
            'reset_link': expected_link,
            'user': email.user,
        })

    assert reset.user == email.user
    assert len(mail.outbox) == 1

    sent = mail.outbox[0]

    assert sent.subject == 'Instructions to Reset Your Know Me Password'
    assert sent.body == expected_content
    assert sent.to == [email.email]


def test_create_and_send_unverified_email(email_factory):
    """
    If the provided email address is not verified, no email should be
    sent.
    """
    email = email_factory(verified=False)

    reset = models.PasswordReset.create_and_send(email.email)

    assert reset is None
    assert len(mail.outbox) == 0


def test_string_conversion(password_reset_factory):
    """
    Converting a password reset into a string should return info about
    the password reset.
    """
    reset = password_reset_factory()
    expected = 'Password reset for {user}'.format(user=reset.user)

    assert str(reset) == expected
