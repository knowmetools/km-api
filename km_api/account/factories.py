"""Factories to generate test instances of ``account`` models.
"""

from django.conf import settings
from django.utils.crypto import get_random_string

import factory

from account import models


class EmailFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``EmailAddress`` instances.
    """
    email = factory.Sequence(lambda n: 'test{n}@example.com'.format(n=n))
    user = factory.SubFactory('factories.UserFactory')

    class Meta:
        model = models.EmailAddress


class EmailConfirmationFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``EmailConfirmation`` instances.
    """
    email = factory.SubFactory('account.factories.EmailFactory')
    key = factory.LazyFunction(
        lambda: get_random_string(
            length=settings.EMAIL_CONFIRMATION_KEY_LENGTH))

    class Meta:
        model = models.EmailConfirmation


class PasswordResetFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``PasswordReset`` instances.
    """
    key = factory.LazyFunction(lambda: get_random_string(
        length=settings.PASSWORD_RESET_KEY_LENGTH))
    user = factory.SubFactory('factories.UserFactory')

    class Meta:
        model = models.PasswordReset
