"""Factories to generate model instances for testing.
"""
import datetime
import hashlib

import factory
from django.utils import timezone

from know_me import models


class AppleReceiptFactory(factory.DjangoModelFactory):
    """
    Factory for generating :class:`AppleReceipt` instances.
    """

    receipt_data = factory.Sequence(lambda n: f"receipt-data-{n}")
    receipt_data_hash = factory.LazyAttribute(
        lambda r: models.AppleReceipt.hash_data(r.receipt_data)
    )
    subscription = factory.SubFactory("know_me.factories.SubscriptionFactory")
    transaction_id = factory.Sequence(str)

    class Meta:
        model = "know_me.AppleReceipt"


class ConfigFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``Config`` instances.
    """

    minimum_app_version_ios = "1.2.3"

    class Meta:
        model = "know_me.Config"


class KMUserAccessorFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``KMUserAccessor`` instances.
    """

    email = factory.Sequence(lambda n: "invite{n}@example.com".format(n=n))
    km_user = factory.SubFactory("know_me.factories.KMUserFactory")

    class Meta(object):
        model = "know_me.KMUserAccessor"


class KMUserFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``KMUser`` instances.
    """

    quote = factory.LazyAttribute(
        lambda km_user: "Hi, I'm {name}".format(
            name=km_user.user.get_short_name()
        )
    )
    user = factory.SubFactory("factories.UserFactory")

    class Meta:
        model = "know_me.KMUser"


class LegacyUserFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``LegacyUser`` instances.
    """

    email = factory.Sequence(lambda n: "test{}@example.com".format(n))

    class Meta:
        model = "know_me.LegacyUser"


class SubscriptionAppleDataFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``SubscriptionAppleData`` instances.
    """

    expiration_time = factory.LazyFunction(
        lambda: timezone.now() + datetime.timedelta(minutes=30)
    )
    latest_receipt_data = factory.LazyAttribute(
        lambda receipt: receipt.receipt_data
    )
    latest_receipt_data_hash = factory.LazyAttribute(
        lambda receipt: hashlib.sha256(
            receipt.latest_receipt_data.encode()
        ).hexdigest()
    )
    receipt_data = factory.Sequence(lambda n: f"bogus receipt data {n}")
    receipt_data_hash = factory.LazyAttribute(
        lambda instance: hashlib.sha256(
            instance.receipt_data.encode()
        ).hexdigest()
    )
    subscription = factory.SubFactory("know_me.factories.SubscriptionFactory")

    class Meta:
        model = "know_me.SubscriptionAppleData"


class SubscriptionFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``Subscription`` instances.
    """

    is_active = True
    user = factory.SubFactory("factories.UserFactory")

    class Meta:
        model = "know_me.Subscription"
