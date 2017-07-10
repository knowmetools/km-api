"""Fixtures for testing the ``mailing_list`` module.
"""

from unittest import mock

import pytest

from mailing_list import factories


@pytest.fixture
def mailchimp_user_factory(db):
    """
    Fixture to get the factory used to create MailChimp users.

    Returns:
        The factory class used to create ``MailchimpUser`` instances.
    """
    return factories.MailchimpUserFactory


@pytest.fixture
def mock_mc_client(settings):
    """
    Fixture to get a mock implementation of the MailChimp client.

    This enables MailChimp integration by default.

    Returns:
        A ``unittest.mock.Mock`` instance that mimics the MailChimp
        client from the ``mailchimp3`` package.
    """
    client = mock.Mock(name='Mock Mailchimp Client')
    client.lists = mock.Mock(name='Mock Lists')
    client.lists.members = mock.Mock(name='Mock Members')
    client.lists.members.update = mock.Mock(name='Mock Update Member')

    return client
