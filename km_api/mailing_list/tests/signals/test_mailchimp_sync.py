from unittest import mock

from mailing_list.signals import mailchimp_sync


@mock.patch(
    'mailing_list.signals.mailchimp_utils.sync_mailchimp_data',
    autospec=True)
def test_sync_mailchimp_disabled(mock_sync, settings):
    """
    If the ``MAILCHIMP_ENABLED`` setting is ``False``, no user data
    should be synced to MailChimp.
    """
    settings.MAILCHIMP_ENABLED = False

    mailchimp_sync(None)

    assert mock_sync.call_count == 0


@mock.patch(
    'mailing_list.signals.mailchimp_utils.sync_mailchimp_data',
    autospec=True)
def test_sync_mailchimp_enabled(mock_sync, settings):
    """
    If the ``MAILCHIMP_ENABLED`` setting is ``True``, user data should
    be synced to MailChimp.
    """
    settings.MAILCHIMP_API_KEY = 'foo'
    settings.MAILCHIMP_ENABLED = True
    settings.MAILCHIMP_LIST_ID = 'list'

    mailchimp_sync(None)

    assert mock_sync.call_count == 1
