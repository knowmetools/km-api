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


class MediaResourceFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``MediaResource`` instances.
    """
    name = factory.Sequence(lambda n: 'Media Resource {n}'.format(n=n))
    profile = factory.SubFactory('know_me.factories.ProfileFactory')
    file = factory.LazyFunction(create_file)

    class Meta:
        model = models.MediaResource


class KMUserFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``KMUser`` instances.
    """
    user = factory.SubFactory('factories.UserFactory')

    class Meta:
        model = models.KMUser


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


class ProfileItemFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``ProfileItem`` instances.
    """
    name = factory.Sequence(lambda n: 'Profile Item {n}'.format(n=n))
    topic = factory.SubFactory('know_me.factories.ProfileTopicFactory')

    class Meta:
        model = models.ProfileItem


class ProfileTopicFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``ProfileTopic`` instances.
    """
    group = factory.SubFactory('know_me.factories.ProfileGroupFactory')
    name = factory.Sequence(lambda n: 'Profile Topic {n}'.format(n=n))
    topic_type = models.ProfileTopic.TEXT

    class Meta:
        model = models.ProfileTopic
