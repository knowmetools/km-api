from unittest import mock

from mailing_list import mailchimp_utils


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
