from unittest import mock

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


def test_update_user(mailchimp_user_factory, mock_mc_client):
    """
    If the user already exists, their details should be updated.
    """
    mailchimp_user = mailchimp_user_factory()
    user = mailchimp_user.user

    mock_mc_client.lists.members.update.return_value = {
        'id': 'new-hash',
    }

    with mock.patch(
            'mailing_list.mailchimp_utils._get_client',
            return_value=mock_mc_client):
        mailchimp_utils.sync_mailchimp_data('list', user)

    assert mock_mc_client.lists.members.update.call_count == 1
    assert mock_mc_client.lists.members.update.call_args[1] == {
        'data': mailchimp_utils.get_member_info(user),
        'list_id': 'list',
        'subscriber_hash': mailchimp_user.subscriber_hash,
    }

    assert models.MailchimpUser.objects.count() == 1

    mailchimp_user.refresh_from_db()

    assert mailchimp_user.subscriber_hash == \
        mock_mc_client.lists.members.update.return_value['id']
