"""Factories to generate model instances for testing.
"""

import factory


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
    email = factory.Sequence(lambda n: 'invite{n}@example.com'.format(n=n))
    km_user = factory.SubFactory('know_me.factories.KMUserFactory')

    class Meta(object):
        model = 'know_me.KMUserAccessor'


class KMUserFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``KMUser`` instances.
    """
    quote = factory.LazyAttribute(lambda km_user: "Hi, I'm {name}".format(
        name=km_user.user.get_short_name()))
    user = factory.SubFactory('factories.UserFactory')

    class Meta:
        model = 'know_me.KMUser'


class LegacyUserFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``LegacyUser`` instances.
    """
    email = factory.Sequence(lambda n: 'test{}@example.com'.format(n))

    class Meta:
        model = 'know_me.LegacyUser'


class SubscriptionAppleDataFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``SubscriptionAppleData`` instances.
    """
    receipt_data = 'bogus receipt data'
    subscription = factory.SubFactory('know_me.factories.SubscriptionFactory')

    class Meta:
        model = 'know_me.SubscriptionAppleData'


class SubscriptionFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``Subscription`` instances.
    """
    is_active = True
    user = factory.SubFactory('factories.UserFactory')

    class Meta:
        model = 'know_me.Subscription'
