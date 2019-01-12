"""Model managers for models in the ``account`` module.
"""

from django.contrib.auth.models import BaseUserManager


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
        kwargs["is_staff"] = True
        kwargs["is_superuser"] = True

        return self.create_user(*args, **kwargs)

    def create_user(self, first_name, last_name, password, **kwargs):
        """
        Create a new ``User`` instance.

        Args:
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
        user = self.model(first_name=first_name, last_name=last_name, **kwargs)
        user.set_password(password)
        user.save()

        return user
