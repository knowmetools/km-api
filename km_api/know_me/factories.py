"""Factories to generate model instances for testing.
"""

import factory

from know_me import models


class ConfigFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``Config`` instances.
    """
    minimum_app_version_ios = '1.2.3'

    class Meta:
        model = 'know_me.Config'


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
