from unittest import mock

from account import models


def test_confirm(email_confirmation_factory):
    """
    Confirming an email should mark the email as verified and then
    delete the confirmation.
    """
    confirmation = email_confirmation_factory()

    with mock.patch(
            'account.models.EmailAddress.verify',
            autospec=True) as mock_verify:
        confirmation.confirm()

    assert mock_verify.call_count == 1
    assert models.EmailConfirmation.objects.count() == 0


def test_create(email_factory):
    """
    Test creating a new email confirmation.
    """
    models.EmailConfirmation.objects.create(
        email=email_factory(),
        key='key')


def test_is_expired_false(email_confirmation_factory, settings):
    """
    If the number of days specified in the
    ``EMAIL_CONFIRMATION_EXPIRATION_DAYS`` setting has not passed since
    the creation of the confirmation, it should not be expired.
    """
    settings.EMAIL_CONFIRMATION_EXPIRATION_DAYS = 1

    confirmation = email_confirmation_factory()

    assert not confirmation.is_expired()


def test_is_expired_true(email_confirmation_factory, settings):
    """
    If the number of days specified in the
    ``EMAIL_CONFIRMATION_EXPIRATION_DAYS`` setting has passed since the
    creation of the confirmation, it should be expired.
    """
    settings.EMAIL_CONFIRMATION_EXPIRATION_DAYS = 0

    confirmation = email_confirmation_factory()

    assert confirmation.is_expired()


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
    expected_context = {
        'confirmation_link': expected_link,
        'user': confirmation.email.user,
    }

    with mock.patch(
            'account.models.templated_email.send_email',
            autospec=True) as mock_send_email:
        confirmation.send_confirmation()

    assert mock_send_email.call_count == 1
    assert mock_send_email.call_args[1] == {
        'context': expected_context,
        'subject': 'Please Confirm Your Know Me Email',
        'template': 'account/email/confirm-email',
        'to': confirmation.email.email,
    }


def test_string_conversion(email_confirmation_factory):
    """
    Converting an email confirmation to a string should return a message
    indicating who the confirmation is for.
    """
    confirmation = email_confirmation_factory()
    expected = 'Confirmation for {email}'.format(
        email=confirmation.email.email)

    assert str(confirmation) == expected
