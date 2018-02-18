"""Factories to generate model instances for testing.
"""

import factory

from know_me import models


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
