from unittest import mock

from requests.exceptions import HTTPError

from mailing_list import mailchimp_utils, models


def test_create_member(mock_mc_client, user_factory):
    """
    If there is no existing list member for the user, one should be
    created.
    """
    user = user_factory()

    mock_mc_client.lists.members.create.return_value = {
        'id': 'hash',
    }

    with mock.patch(
            'mailing_list.mailchimp_utils._get_client',
            return_value=mock_mc_client):
        mailchimp_utils._member_create('list', user)

    expected_data = mailchimp_utils.get_member_info(user)
    expected_data.update({
        'status': 'subscribed',
    })

    assert mock_mc_client.lists.members.create.call_count == 1
    assert mock_mc_client.lists.members.create.call_args[1] == {
        'data': expected_data,
        'list_id': 'list',
    }

    assert models.MailchimpUser.objects.count() == 1

    mailchimp_user = models.MailchimpUser.objects.get()

    assert mailchimp_user.subscriber_hash == \
        mock_mc_client.lists.members.create.return_value['id']
    assert mailchimp_user.user == user


def test_create_member_exists(mock_mc_client, user_factory):
    """
    If the user exists in the mailing list but we don't have a record of
    the user, we should try to update the list member's info instead.
    """
    user = user_factory()

    def mock_create(*args, **kwargs):
        """
        Raise a ``HttpError`` exception.
        """
        raise HTTPError()

    mock_mc_client.lists.members.create.side_effect = mock_create
    mock_mc_client.lists.members.update.return_value = {
        'id': 'new-hash',
    }

    with mock.patch(
            'mailing_list.mailchimp_utils._get_client',
            return_value=mock_mc_client):
        mailchimp_utils._member_create('list', user)

    assert mock_mc_client.lists.members.update.call_count == 1
    assert mock_mc_client.lists.members.update.call_args[1] == {
        'data': mailchimp_utils.get_member_info(user),
        'list_id': 'list',
        'subscriber_hash': user.email,
    }

    assert models.MailchimpUser.objects.count() == 1

    mailchimp_user = models.MailchimpUser.objects.get()

    assert mailchimp_user.subscriber_hash == \
        mock_mc_client.lists.members.update.return_value['id']
    assert mailchimp_user.user == user
