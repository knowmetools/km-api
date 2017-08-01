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
