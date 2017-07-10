from unittest import mock

from requests.exceptions import HTTPError

from mailing_list import mailchimp_utils, models


def test_update_user(mailchimp_user_factory, mock_mc_client):
    """
    If the user already exists, their details should be updated.
    """
    mailchimp_user = mailchimp_user_factory()
    subscriber_hash = mailchimp_user.subscriber_hash
    user = mailchimp_user.user

    mock_mc_client.lists.members.update.return_value = {
        'id': 'new-hash',
    }

    with mock.patch(
            'mailing_list.mailchimp_utils._get_client',
            return_value=mock_mc_client):
        mailchimp_utils._member_update('list', user, mailchimp_user)

    assert mock_mc_client.lists.members.update.call_count == 1
    assert mock_mc_client.lists.members.update.call_args[1] == {
        'data': mailchimp_utils.get_member_info(user),
        'list_id': 'list',
        'subscriber_hash': subscriber_hash,
    }

    assert models.MailchimpUser.objects.count() == 1

    mailchimp_user.refresh_from_db()

    assert mailchimp_user.subscriber_hash == \
        mock_mc_client.lists.members.update.return_value['id']


def test_update_user_nonexistent(mailchimp_user_factory, mock_mc_client):
    """
    If we have a record of a mailing list member but that member doesn't
    exist, the member should be created and the record updated.
    """
    mailchimp_user = mailchimp_user_factory()
    user = mailchimp_user.user

    mock_mc_client.lists.members.update.side_effect = HTTPError
    mock_mc_client.lists.members.create.return_value = {
        'id': 'hash',
    }

    with mock.patch(
            'mailing_list.mailchimp_utils._get_client',
            return_value=mock_mc_client):
        mailchimp_utils.sync_mailchimp_data('list', user)

    expected_data = mailchimp_utils.get_member_info(user)
    expected_data.update({'status': 'subscribed'})

    assert mock_mc_client.lists.members.create.call_count == 1
    assert mock_mc_client.lists.members.create.call_args[1] == {
        'data': expected_data,
        'list_id': 'list',
    }

    assert models.MailchimpUser.objects.count() == 1

    mailchimp_user.refresh_from_db()

    assert mailchimp_user.subscriber_hash == \
        mock_mc_client.lists.members.create.return_value['id']
