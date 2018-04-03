from unittest import mock

from rest_email_auth.models import EmailAddress

from mailing_list import mailchimp_utils, models


def test_create_user(mock_mc_client, user_factory):
    """
    If there is no existing list member for the user, one should be
    created.
    """
    user = user_factory()

    with mock.patch(
            'mailing_list.mailchimp_utils._member_create',
            autospec=True) as mock_create:
        mailchimp_utils.sync_mailchimp_data('list', user)

    assert mock_create.call_count == 1
    assert mock_create.call_args[0] == ('list', user)


@mock.patch(
    'mailing_list.mailchimp_utils._member_create',
    autospec=True,
    side_effect=EmailAddress.DoesNotExist)
def test_create_user_missing_email(mock_create, mock_mc_client, user_factory):
    """
    If the user has no primary email address, the update should abort.

    Regression test for #295.
    """
    user = user_factory()
    user.email_addresses.all().delete()

    mailchimp_utils.sync_mailchimp_data('list', user)

    assert models.MailchimpUser.objects.count() == 0


def test_update_user(mailchimp_user_factory, mock_mc_client):
    """
    If the user already exists, their details should be updated.
    """
    mailchimp_user = mailchimp_user_factory()
    user = mailchimp_user.user

    with mock.patch(
            'mailing_list.mailchimp_utils._member_update',
            autospec=True) as mock_update:
        mailchimp_utils.sync_mailchimp_data('list', user)

    assert mock_update.call_count == 1
    assert mock_update.call_args[0] == ('list', user, mailchimp_user)
