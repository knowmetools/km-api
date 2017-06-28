import pytest

from km_auth.tests.conftest import user_factory     # noqa

from know_me import factories


@pytest.fixture
def profile_factory(db):
    """
    Fixture to get the factory used for generating ``Profile`` objects.

    Returns:
        The factory class used to create test ``Profile`` instances.
    """
    return factories.ProfileFactory
