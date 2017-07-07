"""Fixtures for testing the ``mailing_list`` module.
"""

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
