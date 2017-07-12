"""Model managers for models in the ``account`` module.
"""

from django.conf import settings
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
