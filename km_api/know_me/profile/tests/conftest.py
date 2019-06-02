import pytest

from know_me.profile import factories


@pytest.fixture
def list_entry_factory(db):
    """
    Fixture to get the factory used to create list entries.
    """
    return factories.ListEntryFactory
