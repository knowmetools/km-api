"""Factories to generate model instances for testing.
"""

from django.core.files.base import ContentFile

import factory

from know_me import models


def create_file():
    """
    Create a simple text file.

    Returns:
        A simple text file represented as a ``ContentFile`` instance.
    """
    return ContentFile(
        content='The quick brown fox jumped over the lazy dog.',
        name='foo.txt')


class GalleryItemFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``GalleryItem`` instances.
    """
    name = factory.Sequence(lambda n: 'Gallery Item {n}'.format(n=n))
    profile = factory.SubFactory('know_me.factories.ProfileFactory')
    resource = factory.LazyFunction(create_file)

    class Meta:
        model = models.GalleryItem


class ProfileFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``Profile`` instances.
    """
    name = 'John'
    quote = factory.LazyAttribute(lambda profile: "Hi, I'm {name}".format(
        name=profile.name))
    user = factory.SubFactory('factories.UserFactory')
    welcome_message = 'Life is like a box of chocolates.'

    class Meta:
        model = models.Profile


class ProfileGroupFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``ProfileGroup`` instances.
    """
    name = 'Test Profile'
    profile = factory.SubFactory('know_me.factories.ProfileFactory')

    class Meta:
        model = models.ProfileGroup


class ProfileRowFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``ProfileRow`` instances.
    """
    group = factory.SubFactory('know_me.factories.ProfileGroupFactory')
    name = factory.Sequence(lambda n: 'Profile Row {n}'.format(n=n))
    row_type = models.ProfileRow.TEXT

    class Meta:
        model = models.ProfileRow
