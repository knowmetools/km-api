"""Models for the Know Me app.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from rest_framework.reverse import reverse


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

    def get_absolute_url(self):
        """
        Get the absolute URL of the instance's detail view.

        Returns:
            str:
                The absolute URL of the instance's detail view.
        """
        return reverse(
            'know-me:profile-detail',
            kwargs={'profile_pk': self.pk})

    def get_group_list_url(self, request=None):
        """
        Get the absolute URL of the instance's group list view.

        Args:
            request (optional):
                A request used as context when constructing the URL. If
                given, the resulting URL will be a full URI with a
                protocol and domain name.

        Returns:
            str:
                The absolute URL of the instance's group list view.
        """
        return reverse(
            'know-me:profile-group-list',
            kwargs={'profile_pk': self.pk},
            request=request)


class ProfileGroup(models.Model):
    """
    A profile group contains a targeted subset of a ``Profile``.

    Attributes:
        is_default (bool):
            A boolean controlling if the group is the default for its
            parent profile.
        name (str):
            The name of the group.
        profile:
            The ``Profile`` instance the group belongs to.
    """
    is_default = models.BooleanField(
        default=False,
        help_text=_('The default profile group is displayed initially.'),
        verbose_name=_('is default'))
    name = models.CharField(
        max_length=255,
        verbose_name=_('name'))
    profile = models.ForeignKey(
        'know_me.Profile',
        on_delete=models.CASCADE,
        related_name='groups',
        related_query_name='group',
        verbose_name=_('profile'))

    class Meta:
        verbose_name = _('profile group')
        verbose_name_plural = _('profile groups')

    def __str__(self):
        """
        Get a string representation of the profile group.

        Returns:
            str:
                The profile group's name.
        """
        return self.name

    def get_absolute_url(self):
        """
        Get the absolute URL of the instance's detail view.

        Returns:
            The URL of the instance's detail view.
        """
        return reverse(
            'know-me:profile-group-detail',
            kwargs={
                'group_pk': self.pk,
                'profile_pk': self.profile.pk,
            })
