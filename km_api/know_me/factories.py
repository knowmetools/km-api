"""Factories to generate model instances for testing.
"""

import factory

from know_me import models


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
