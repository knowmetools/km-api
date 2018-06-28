"""Models for the ``account`` module.
"""

import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from rest_email_auth.models import EmailAddress

from account import managers


def get_user_image_path(user, filename):
    """
    Get the path where a user's image should be stored.

    Args:
        user:
            The user whose image is being uploaded.
        filename:
            The original name of the uploaded file.

    Returns:
        The path that the image should be uploaded to.
    """
    return 'users/{name}.{ext}'.format(
        ext=filename.rsplit('.', 1)[-1],
        name=uuid.uuid4())


class User(PermissionsMixin, AbstractBaseUser):
    """
    A user's profile.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at'))
    image = models.ImageField(
        blank=True,
        help_text=_('A profile image for the user.'),
        upload_to=get_user_image_path,
        verbose_name=_('profile image'))
    is_active = models.BooleanField(
        default=True,
        help_text=_('Inactive users are not able to log in.'),
        verbose_name=_('is active'))
    is_staff = models.BooleanField(
        default=False,
        help_text=_('Staff users are allowed to access the admin site.'),
        verbose_name=_('is staff'))
    is_superuser = models.BooleanField(
        default=False,
        help_text=_('Super users are given all permissions without them being '
                    'explicitly set.'),
        verbose_name=_('is superuser'))
    first_name = models.CharField(
        max_length=255,
        verbose_name=_('first name'))
    last_name = models.CharField(
        max_length=255,
        verbose_name=_('last name'))
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_('The time that the user was last updated.'),
        verbose_name=_('updated_at'))

    USERNAME_FIELD = 'first_name'

    # Tell Django which fields are required. This is used when commands
    # like ``createsuperuser`` are used. These fields exclude the
    # username and password fields which are included by default.
    # https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#django.contrib.auth.models.CustomUser.REQUIRED_FIELDS
    REQUIRED_FIELDS = ('last_name',)

    # Set custom manager
    objects = managers.UserManager()

    class Meta:
        ordering = ('created_at',)
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Get the user's full name.

        Returns:
            str:
                The user's first and last name.
        """
        return '{first} {last}'.format(
            first=self.first_name,
            last=self.last_name)

    def get_short_name(self):
        """
        Get a short name for the user.

        Returns:
            str:
                The user's first name.
        """
        return self.first_name

    @property
    def primary_email(self):
        """
        The user's primary email address.
        """
        try:
            return self.email_addresses.get(is_primary=True)
        except EmailAddress.DoesNotExist:
            return None
