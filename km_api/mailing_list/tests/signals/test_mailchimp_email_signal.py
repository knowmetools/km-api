from unittest import mock

from django.db.models.signals import post_save

import pytest

from rest_email_auth.models import EmailAddress

from mailing_list.signals import mailchimp_email_signal, mailchimp_user_signal


@pytest.fixture(autouse=True)
def disable_other_signals():
    """
    Disable other signals that cause a sync.
    """
    post_save.disconnect(mailchimp_user_signal, sender=EmailAddress)


@mock.patch(
    'mailing_list.signals.mailchimp_sync',
    autospec=True)
def test_create_email_address(mock_sync, email_factory, user_factory):
    """
    Creating a verified email address should trigger a sync.
    """
    post_save.disconnect(mailchimp_email_signal, sender=EmailAddress)
    user = user_factory()
    post_save.connect(mailchimp_email_signal, sender=EmailAddress)

    email = email_factory(is_verified=True, user=user)

    assert mock_sync.call_count == 1
    assert mock_sync.call_args[0] == (email.user,)


@mock.patch(
    'mailing_list.signals.mailchimp_sync',
    autospec=True)
def test_create_email_address_unverified(
        mock_sync,
        email_factory,
        user_factory):
    """
    Creating an unverified email address should not trigger a MailChimp
    sync.
    """
    post_save.disconnect(mailchimp_email_signal, sender=EmailAddress)
    user = user_factory()
    post_save.connect(mailchimp_email_signal, sender=EmailAddress)

    email_factory(is_verified=False, user=user)

    assert mock_sync.call_count == 0


@mock.patch(
    'mailing_list.signals.mailchimp_sync',
    autospec=True)
def test_update_email(mock_sync, email_factory):
    """
    Updates to an email address should trigger a sync.
    """
    email = email_factory(is_verified=False)

    # We have to track the call count from the user and email address
    # implicitly created by 'email_factory'.
    call_count = mock_sync.call_count

    email.is_verified = True
    email.save()

    assert mock_sync.call_count == call_count + 1
    assert mock_sync.call_args[0] == (email.user,)
