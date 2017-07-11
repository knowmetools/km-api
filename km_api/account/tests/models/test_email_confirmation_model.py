from django.core import mail
from django.template.loader import render_to_string

from account import models


def test_create(user_factory):
    """
    Test creating a new email confirmation.
    """
    models.EmailConfirmation.objects.create(
        key='key',
        user=user_factory())


def test_send_confirmation(email_confirmation_factory, settings):
    """
    The email confirmation should be sent to the email address of the
    user the confirmation links to and it should include the URL given
    by the ``EMAIL_CONFIRMATION_LINK_TEMPLATE`` setting.
    """
    settings.EMAIL_CONFIRMATION_LINK_TEMPLATE = 'example.com/confirm/{key}'

    confirmation = email_confirmation_factory()

    expected_link = settings.EMAIL_CONFIRMATION_LINK_TEMPLATE.format(
        key=confirmation.key)
    expected_content = render_to_string(
        'account/email/confirm-email.txt',
        context={
            'confirmation_link': expected_link,
            'user': confirmation.user,
        })

    confirmation.send_confirmation()

    assert len(mail.outbox) == 1

    email = mail.outbox[0]

    assert email.subject == 'Please Confirm Your Know Me Email'
    assert email.body == expected_content
    assert email.to == [confirmation.user.email]


def test_string_conversion(email_confirmation_factory):
    """
    Converting an email confirmation to a string should return a message
    indicating who the confirmation is for.
    """
    confirmation = email_confirmation_factory()
    expected = 'Confirmation for {email}'.format(email=confirmation.user.email)

    assert str(confirmation) == expected
