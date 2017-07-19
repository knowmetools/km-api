"""Model managers for models in the ``account`` module.
"""

from django.conf import settings
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils.crypto import get_random_string


class EmailAddressManager(models.Manager):
    """
    Manager for email addresses.
    """

    def create(self, **kwargs):
        """
        Create a new email address.

        If this email address is the only address owned by a user, it is
        set as the user's primary address.

        Args:
            kwargs:
                Keyword arguments to create the address with.

        Returns:
            The created ``EmailAddress`` instance.
        """
        user = kwargs['user']
        if not user.email_addresses.filter(primary=True).exists():
            kwargs['primary'] = True

        email = self.model(**kwargs)
        email.save()

        return email


class EmailConfirmationManager(models.Manager):
    """
    Manager for email confirmations.
    """

    def create(self, email, key=None):
        """
        Create a new email confirmation.

        Args:
            email:
                The email address to create the confirmation for. The
                confirmation is sent to this email address.
            key (:obj:`str`, optional):
                The key to use to confirm the email. Defaults to a
                random string whose length is determined by the
                ``EMAIL_CONFIRMATION_KEY_LENGTH`` setting.

        Returns:
            A new ``EmailConfirmation`` instance.
        """
        key = key or get_random_string(
            length=settings.EMAIL_CONFIRMATION_KEY_LENGTH)

        confirmation = self.model(email=email, key=key)
        confirmation.save()

        return confirmation


class PasswordResetManager(models.Manager):
    """
    Manager for password resets.
    """

    def create(self, user, key=None):
        """
        Create a new password reset.

        Args:
            user:
                The user to create the password reset for.
            key (:obj:`str`, optional):
                The key to use to verify the password reset. Defaults to
                a random string whose length is determined by the
                ``PASSWORD_RESET_KEY_LENGTH`` setting.

        Returns:
            A new ``PasswordReset`` instance.
        """
        key = key or get_random_string(
            length=settings.PASSWORD_RESET_KEY_LENGTH)

        reset = self.model(key=key, user=user)
        reset.save()

        return reset


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
