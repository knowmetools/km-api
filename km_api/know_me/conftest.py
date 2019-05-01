"""Fixtures for testing the ``know_me`` module.
"""
from unittest import mock

from django.core.files.base import ContentFile

import pytest

from know_me import factories, models


@pytest.fixture
def mock_apple_receipt_qs():
    mock_queryset = mock.Mock(spec=models.AppleReceipt.objects)
    mock_queryset.all.return_value = mock_queryset
    mock_queryset.filter.return_value = mock_queryset
    mock_queryset.model.DoesNotExist = models.AppleReceipt.DoesNotExist

    with mock.patch(
        "know_me.models.AppleReceipt.objects", new=mock_queryset
    ), mock.patch(
        "know_me.models.AppleReceipt._meta.default_manager", new=mock_queryset
    ):
        yield mock_queryset


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
        content=b"The quick brown fox jumped over the lazy dog.",
        name="foo.txt",
    )


@pytest.fixture
def legacy_user_factory(db):
    """
    Fixture to get the factory used to create legacy users.
    """
    return factories.LegacyUserFactory
