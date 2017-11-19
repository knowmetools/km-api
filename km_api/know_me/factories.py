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


class EmergencyItemFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``EmergencyItem`` instances.
    """
    name = factory.Sequence(lambda n: 'Emergency Item {n}'.format(n=n))
    km_user = factory.SubFactory('know_me.factories.KMUserFactory')

    class Meta:
        model = models.EmergencyItem


class EmergencyContactFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``EmergencyContact`` instances.
    """
    km_user = factory.SubFactory('know_me.factories.KMUserFactory')
    name = factory.Sequence(lambda n: 'Contact Name {n}'.format(n=n))
    relation = 'Caregiver'
    phone_number = '19193334444'

    class Meta:
        model = models.EmergencyContact


class ImageContentFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``ImageContent`` instances.
    """
    profile_item = factory.SubFactory('know_me.factories.ProfileItemFactory')

    class Meta(object):
        model = models.ImageContent


class KMUserAccessorFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``KMUserAccessor`` instances.
    """
    km_user = factory.SubFactory('know_me.factories.KMUserFactory')

    class Meta(object):
        model = models.KMUserAccessor


class KMUserFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``KMUser`` instances.
    """
    quote = factory.LazyAttribute(lambda km_user: "Hi, I'm {name}".format(
        name=km_user.user.get_short_name()))
    user = factory.SubFactory('factories.UserFactory')

    class Meta:
        model = models.KMUser


class ListContentFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``ListContent`` instances.
    """
    profile_item = factory.SubFactory('know_me.factories.ProfileItemFactory')

    class Meta(object):
        model = models.ListContent


class ListEntryFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``ListEntry`` instances.
    """
    list_content = factory.SubFactory('know_me.factories.ListContentFactory')
    text = factory.Sequence(lambda n: 'List entry {n}'.format(n=n))

    class Meta(object):
        model = models.ListEntry


class MediaResourceCategoryFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``MediaResourceCategory`` instances.
    """
    name = factory.Sequence(lambda n: 'Category {n}'.format(n=n))

    class Meta:
        model = 'know_me.MediaResourceCategory'


class MediaResourceFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``MediaResource`` instances.
    """
    name = factory.Sequence(lambda n: 'Media Resource {n}'.format(n=n))
    km_user = factory.SubFactory('know_me.factories.KMUserFactory')
    file = factory.LazyFunction(create_file)

    class Meta:
        model = models.MediaResource


class ProfileFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``Profile`` instances.
    """
    name = 'Test KMUser'
    km_user = factory.SubFactory('know_me.factories.KMUserFactory')

    class Meta:
        model = models.Profile


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
    profile = factory.SubFactory('know_me.factories.ProfileFactory')
    name = factory.Sequence(lambda n: 'Profile Topic {n}'.format(n=n))
    topic_type = models.ProfileTopic.TEXT

    class Meta:
        model = models.ProfileTopic
