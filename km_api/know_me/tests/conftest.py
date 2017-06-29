import pytest

from know_me import factories


@pytest.fixture
def profile_factory(db):
    """
    Fixture to get the factory used for generating ``Profile`` objects.

    Returns:
        The factory class used to create test ``Profile`` instances.
    """
    return factories.ProfileFactory


@pytest.fixture
def profile_group_factory(db):
    """
    Fixture to get the factory used to create profile groups.

    Returns:
        The factory class used to create ``ProfileGroup`` instances.
    """
    return factories.ProfileGroupFactory


@pytest.fixture
def profile_row_factory(db):
    """
    Fixture to get the factory used to create profile rows.

    Returns:
        The factory class used to create ``ProfileRow`` instances.
    """
    return factories.ProfileRowFactory
