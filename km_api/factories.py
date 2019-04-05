"""Factories to create model instances for testing.

These factories are used project-wide.
"""

import factory
from django.contrib.auth import get_user_model
from rest_email_auth.models import EmailAddress


class EmailConfirmationFactory(factory.DjangoModelFactory):
    """
    Factory for generating :class:`EmailConfirmation` instances.
    """

    email = factory.SubFactory("factories.EmailFactory")

    class Meta:
        model = "rest_email_auth.EmailConfirmation"


class EmailFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``EmailAddress`` instances.
    """

    email = factory.Sequence(lambda n: "test{}@example.com".format(n))
    user = factory.SubFactory("factories.UserFactory")

    class Meta:
        model = "rest_email_auth.EmailAddress"


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``User`` instances.
    """

    first_name = "John"
    last_name = "Doe"
    password = "password"

    class Meta:
        model = get_user_model()

    class Params:
        has_premium = factory.Trait(
            know_me_subscription=factory.RelatedFactory(
                factory="know_me.factories.SubscriptionFactory",
                factory_related_name="user",
                is_active=True,
            )
        )

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        """
        Create an email address for the user.
        """
        if obj.email_addresses.count() == 0:
            EmailAddress.objects.create(
                email=f"{obj.first_name}{obj.pk}@example.com",
                is_primary=True,
                is_verified=True,
                user=obj,
            )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Use the user manager's ``create_user`` method.

        We use this method to ensure that the user's password is stored
        correctly.

        Args:
            model_class:
                The class we're creating a new instance of.
            args:
                Positional arguments to pass to the ``create_user``
                method.
            kwargs:
                Keyword arguments to pass to the ``create_user`` method.

        Returns:
            The newly created ``User`` instance.
        """
        manager = cls._get_manager(model_class)

        return manager.create_user(*args, **kwargs)
