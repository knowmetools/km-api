from unittest import mock


def test_mailchimp_disabled(settings, user_factory):
    """
    If the ``MAILCHIMP_ENABLED`` setting is ``False``, no user data
    should be synced to MailChimp.
    """
    settings.MAILCHIMP_ENABLED = False

    with mock.patch(
            'mailing_list.signals.mailchimp_utils.sync_mailchimp_data',
            autospec=True) as mock_sync:
        user_factory()

    assert mock_sync.call_count == 0


def test_user_creation(settings, user_factory):
    """
    When a user is created, their data should be synced to MailChimp.
    """
    settings.MAILCHIMP_ENABLED = True
    settings.MAILCHIMP_LIST_ID = '123456'

    with mock.patch(
            'mailing_list.signals.mailchimp_utils.sync_mailchimp_data',
            autospec=True) as mock_sync:
        user = user_factory()

    assert mock_sync.call_count == 1
    assert mock_sync.call_args[0] == (settings.MAILCHIMP_LIST_ID, user)


def test_user_save(settings, user_factory):
    """
    When a user's information is updated, the updated data should be
    synced to MailChimp.
    """
    user = user_factory(first_name='Bob')

    settings.MAILCHIMP_ENABLED = True
    settings.MAILCHIMP_LIST_ID = '123456'

    with mock.patch(
            'mailing_list.signals.mailchimp_utils.sync_mailchimp_data',
            autospec=True) as mock_sync:
        user.first_name = 'John'
        user.save()

    assert mock_sync.call_count == 1
    assert mock_sync.call_args[0] == (settings.MAILCHIMP_LIST_ID, user)
