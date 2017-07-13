"""Models for the ``account`` module.
"""

import datetime

from django.conf import settings
from django.core import mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext, ugettext_lazy as _

from account import managers


class EmailAddress(models.Model):
    """
    Model to track an email address for a user.
    """
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name=_('email'))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='email_addresses',
        related_query_name='email_address',
        verbose_name=_('user'))
    verified = models.BooleanField(
        default=False,
        verbose_name=_('verified'))

    class Meta:
        verbose_name = _('email address')
        verbose_name_plural = _('email addresses')

    def __str__(self):
        """
        Get a string representation of the address.

        Returns:
            str:
                The instance's ``email`` attribute.
        """
        return self.email


class EmailConfirmation(models.Model):
    """
    Model that allows validation of an email address.

    The confirmation contains a link to a user, a key, and an expiration
    date. An email can be validated by checking that the confirmation
    has not expired and that the provided key matches the confirmation's
    key.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at'))
    key = models.CharField(
        max_length=settings.EMAIL_CONFIRMATION_KEY_LENGTH,
        unique=True,
        verbose_name=_('key'))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('user'))

    objects = managers.EmailConfirmationManager()

    class Meta:
        verbose_name = _('email confirmation')
        verbose_name_plural = _('email confirmations')

    def __str__(self):
        """
        Get a string representation of the instance.

        Returns:
            str:
                A string containing a message indicating which email
                address the confirmation is for.
        """
        return ugettext(
            'Confirmation for %(email)s' % {
                'email': self.user.email,
            })

    def is_expired(self):
        """
        Determine if the confirmation has expired.

        The duration that a confirmation is valid for is specified in
        the ``EMAIL_CONFIRMATION_EXPIRATION_DAYS`` setting.

        Returns:
            bool:
                ``True`` if the confirmation has expired and ``False``
                otherwise.
        """
        now = timezone.now()
        expiration = self.created_at + datetime.timedelta(
            days=settings.EMAIL_CONFIRMATION_EXPIRATION_DAYS)

        return now > expiration

    def send_confirmation(self):
        """
        Send a confirmation email to the linked user's address.
        """
        confirmation_link = settings.EMAIL_CONFIRMATION_LINK_TEMPLATE.format(
            key=self.key)
        context = {
            'confirmation_link': confirmation_link,
            'user': self.user,
        }
        text_content = render_to_string(
            'account/email/confirm-email.txt',
            context)

        mail.send_mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            message=text_content,
            recipient_list=[self.user.email],
            subject=ugettext('Please Confirm Your Know Me Email'))


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
    email_verified = models.BooleanField(
        default=False,
        help_text=_('Users without a verified email address may not log in.'),
        verbose_name=_('email verified'))
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

    def send_password_changed_email(self):
        """
        Send an email notifying the user their password was changed.
        """
        text_content = render_to_string(
            'account/email/password-changed.txt',
            {
                'user': self,
            })

        mail.send_mail(
            _('Your Know Me Password was Changed'),
            message=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email])
