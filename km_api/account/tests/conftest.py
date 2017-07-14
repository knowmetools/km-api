"""Fixtures for testing the ``account`` module.
"""

import pytest

from account import authentication, factories


@pytest.fixture
def auth_backend():
    """
    Get an instance of the account authentication backend.

    Returns:
        An instance of ``authentication.AuthenticationBackend``.
    """
    return authentication.AuthenticationBackend()


@pytest.fixture
def email_confirmation_factory(db):
    """
    Get the factory used to create email confirmations.

    Returns:
        The factory class used to create ``EmailConfirmation``
        instances.
    """
    return factories.EmailConfirmationFactory


@pytest.fixture
def email_factory(db):
    """
    Get the factory used to create email addresses.

    Returns:
        The factory class used to create ``EmailAddress`` instances.
    """
    return factories.EmailFactory