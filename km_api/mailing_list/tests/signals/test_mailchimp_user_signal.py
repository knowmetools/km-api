from unittest import mock

from django.db.models.signals import post_save

import pytest

from rest_email_auth.models import EmailAddress

from mailing_list.signals import mailchimp_email_signal


@pytest.fixture(autouse=True)
def disable_other_signals():
    """
    Disable other signals that cause a sync.
    """
    post_save.disconnect(mailchimp_email_signal, sender=EmailAddress)


@mock.patch(
    'mailing_list.signals.mailchimp_sync',
    autospec=True)
def test_create_user(mock_sync, user_factory):
    """
    Creating a new user should not trigger the MailChimp sync.

    We have to manually create the user because the user factory creates
    an email address for the user.
    """
    user_factory()

    assert mock_sync.call_count == 0


@mock.patch(
    'mailing_list.signals.mailchimp_sync',
    autospec=True)
def test_update_user(mock_sync, user_factory):
    """
    Updating an existing user's information should trigger the MailChimp
    sync.
    """
    user = user_factory(first_name='Bob')

    user.first_name = 'John'
    user.save()

    assert mock_sync.call_count == 1
    assert mock_sync.call_args[0] == (user,)
