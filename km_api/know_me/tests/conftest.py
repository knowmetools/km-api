"""Fixtures for testing the ``know_me`` module.
"""

from django.core.files.base import ContentFile

import pytest

from know_me import factories


@pytest.fixture
def emergency_item_factory(db):
    """
    Fixture to get the factory used to create emergency items.

    Returns:
        The factory class used to create test ``EmergencyItem`` instances.
    """
    return factories.EmergencyItemFactory


@pytest.fixture
def file():
    """
    Fixture to get a file suitable for a ``FileField``.

    Returns:
        A simple text file.
    """
    return ContentFile(
        content=b'The quick brown fox jumped over the lazy dog.',
        name='foo.txt')


@pytest.fixture
def image_content_factory(db):
    """
    Fixture to get the factory used to create profile item image
    content.

    Returns:
        The factory class used to create test ``ImageContent``
        instances.
    """
    return factories.ImageContentFactory


@pytest.fixture
def km_user_factory(db):
    """
    Fixture to get the factory used to create a Know Me User.

    Returns:
        The factory class used to create test ``KMUser`` instances.
    """
    return factories.KMUserFactory


@pytest.fixture
def emergency_contact_factory(db):
    """
    Fixture to get the factory used to create an Emergency Contact.

    Returns:
        The factory class used to create test ``EmergencyContact`` instances.
    """
    return factories.EmergencyContactFactory


@pytest.fixture
def list_content_factory(db):
    """
    Fixture to get the factory used to create profile item list content.

    Returns:
        :class:`.ListContentFactory`:
            The factory class used to create test :class:`.ListContent`
            instances.
    """
    return factories.ListContentFactory


@pytest.fixture
def list_entry_factory(db):
    """
    Fixture to get the factory used to create list entries.

    Returns:
        :class:`.ListEntryFactory`:
            The factory class used to create test :class:`.ListEntry`
            instances.
    """
    return factories.ListEntryFactory


@pytest.fixture
def media_resource_factory(db):
    """
    Fixture to get the factory used to create media resource.

    Returns:
        The factory class used to create test ``MediaResource`` instances.
    """
    return factories.MediaResourceFactory


@pytest.fixture
def profile_factory(db):
    """
    Fixture to get the factory used to create profiles.

    Returns:
        The factory class used to create ``Profile`` instances.
    """
    return factories.ProfileFactory


@pytest.fixture
def profile_item_factory(db):
    """
    Fixture to get the factory used to create profile items.

    Returns:
        The factory class used to create ``ProfileItem`` instances.
    """
    return factories.ProfileItemFactory


@pytest.fixture
def profile_topic_factory(db):
    """
    Fixture to get the factory used to create profile topics.

    Returns:
        The factory class used to create ``ProfileTopic`` instances.
    """
    return factories.ProfileTopicFactory
