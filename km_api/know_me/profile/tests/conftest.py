import pytest

from know_me.profile import factories


@pytest.fixture
def list_entry_factory(db):
    """
    Fixture to get the factory used to create list entries.
    """
    return factories.ListEntryFactory


@pytest.fixture
def media_resource_factory(db):
    """
    Fixture to get the factory used to create media resources.
    """
    return factories.MediaResourceFactory


@pytest.fixture
def profile_factory(db):
    """
    Fixture to get the factory used to create profiles.
    """
    return factories.ProfileFactory


@pytest.fixture
def profile_item_factory(db):
    """
    Fixture to get the factory used to create profile items.
    """
    return factories.ProfileItemFactory


@pytest.fixture
def profile_topic_factory(db):
    """
    Fixture to get the factory used to create profile topics.
    """
    return factories.ProfileTopicFactory
