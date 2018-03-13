import pytest

from know_me.journal import factories


@pytest.fixture
def entry_factory(db):
    """
    Fixture to get the factory used to create journal entries.
    """
    return factories.EntryFactory
