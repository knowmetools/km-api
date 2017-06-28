"""Models for the Know Me app.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):
    """
    A profile contains information about a specific user.

    Attributes:
        name (str):
            The user's name.
        quote (str):
            A quote from the user.
        user:
            The user who owns this profile.
        welcome_message (str):
            A message to welcome other users to the profile.
    """
    name = models.CharField(
        max_length=255,
        verbose_name=_('name'))
    quote = models.TextField(verbose_name=_('quote'))
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('user'))
    welcome_message = models.TextField(verbose_name=_('welcome message'))

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        """
        Get a string representation of the profile.

        Returns:
            str:
                The profile's name.
        """
        return self.name
