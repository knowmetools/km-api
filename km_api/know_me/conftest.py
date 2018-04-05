"""Fixtures for testing the ``know_me`` module.
"""

from django.core.files.base import ContentFile

import pytest

from know_me import factories


@pytest.fixture
def config_factory(db):
    """
    Fixture to get the factory used to create ``Config`` instances.
    """
    return factories.ConfigFactory


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
def km_user_accessor_factory(db):
    """
    Fixture to get the factory used to create km user accessors.

    Returns:
        The factory class used to create ``KMUser Access`` instances.
    """
    return factories.KMUserAccessorFactory


@pytest.fixture
def km_user_factory(db):
    """
    Fixture to get the factory used to create a Know Me User.

    Returns:
        The factory class used to create test ``KMUser`` instances.
    """
    return factories.KMUserFactory
