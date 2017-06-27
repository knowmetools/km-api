"""Fixtures for pytest.
"""

import pytest

from km_auth import factories


@pytest.fixture
def user_factory(db):
    """
    Fixture to get the class used to create ``User`` instances.

    Returns:
        ``km_auth.factories.UserFactory``
    """
    return factories.UserFactory
