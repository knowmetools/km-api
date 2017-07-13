"""Model managers for models in the ``account`` module.
"""

from django.conf import settings
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils.crypto import get_random_string


class EmailConfirmationManager(models.Manager):
    """
    Manager for email confirmations.
    """

    def create(self, user, key=None):
        """
        Create a new email confirmation.

        Args:
            user:
                The user to create the confirmation for. The
                confirmation is sent to the user's email.
            key (:obj:`str`, optional):
                The key to use to confirm the email. Defaults to a
                random string whose length is determined by the
                ``EMAIL_CONFIRMATION_KEY_LENGTH`` setting.

        Returns:
            A new ``EmailConfirmation`` instance.
        """
        key = key or get_random_string(
            length=settings.EMAIL_CONFIRMATION_KEY_LENGTH)

        confirmation = self.model(key=key, user=user)
        confirmation.save()

        return confirmation


class UserManager(BaseUserManager):
    """
    Manager for the ``User`` model.
    """

    def create_superuser(self, *args, **kwargs):
        """
        Create a new superuser.

        This is a wrapper around ``create_user`` that sets the
        ``is_staff`` and ``is_superuser`` flags to ``True``.

        Args:
            args:
                Positional arguments to pass to ``create_user``.
            kwargs:
                Keyword arguments to pass to ``create_user``.

        Returns:
            The new superuser instance.
        """
        kwargs['is_staff'] = True
        kwargs['is_superuser'] = True

        return self.create_user(*args, **kwargs)

    def create_user(self, email, first_name, last_name, password, **kwargs):
        """
        Create a new ``User`` instance.

        Args:
            email (str):
                The user's email address.
            first_name (str):
                The user's first name.
            last_name (str):
                The user's last name.
            password (str):
                The user's password.
            kwargs:
                Any additional keyword arguments to pass to the user
                instance.

        Returns:
            A new ``User`` instance with the given attributes.
        """
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **kwargs)
        user.set_password(password)
        user.save()

        return user
