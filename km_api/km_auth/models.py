"""Models dealing with user authentication.
"""

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from km_auth import managers


class User(PermissionsMixin, AbstractBaseUser):
    """
    A user's profile.

    Attributes:
        email (str):
            The user's email address.
        is_active (bool):
            A boolean indicating if the user is active. Inactive users
            are not able to log in.
        is_staff (bool):
            A boolean indicating if the user is staff. Staff users are
            able to access the admin site.
        is_superuser (bool):
            A boolean indicating if the user is a superuser. Superusers
            have all permissions without them being explicitly granted.
        first_name (str):
            The user's first name.
        last_name (str):
            The user's last name.
    """
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name=_('email'))
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

    # Let Django know about specific fields
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    # Tell Django which fields are required. This is used when commands
    # like ``createsuperuser`` are used. These fields exclude the
    # username and password fields which are included by default.
    # https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#django.contrib.auth.models.CustomUser.REQUIRED_FIELDS
    REQUIRED_FIELDS = ('first_name', 'last_name')

    # Set custom manager
    objects = managers.UserManager()

    class Meta:
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
