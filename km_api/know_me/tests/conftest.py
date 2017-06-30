"""Fixtures for testing the ``know_me`` module.
"""

from django.core.files.base import ContentFile

import pytest

from know_me import factories


@pytest.fixture
def file():
    """
    Fixture to get a file suitable for a ``FileField``.

    Returns:
        A simple text file.
    """
    return ContentFile(
        content='The quick brown fox jumped over the lazy dog.',
        name='foo.txt')


@pytest.fixture
def gallery_item_factory(db):
    """
    Fixture to get the factory used to create gallery items.

    Returns:
        The factory class used to create test ``GalleryItem`` instances.
    """
    return factories.GalleryItemFactory


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
