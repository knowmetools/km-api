"""Factories to create model instances for testing.

These factories are used project-wide.
"""

from django.contrib.auth import get_user_model

import factory


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``User`` instances.
    """
    email = factory.Sequence(lambda n: 'test{n}@example.com'.format(n=n))
    first_name = 'John'
    last_name = 'Doe'
    password = 'password'

    class Meta:
        model = get_user_model()

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
