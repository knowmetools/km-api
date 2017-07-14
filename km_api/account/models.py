"""Models for the ``account`` module.
"""

from collections import namedtuple
import datetime
import logging

from django.conf import settings
from django.core import mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext, ugettext_lazy as _

from rest_framework.reverse import reverse

from permission_utils import model_mixins as mixins

from account import managers


logger = logging.getLogger(__name__)


EmailAction = namedtuple('EmailAction', ['id', 'label'])


class EmailAddress(mixins.IsAuthenticatedMixin, models.Model):
    """
    Model to track an email address for a user.
    """
    NOOP = 1
    REPLACE_PRIMARY = 2

    VERIFIED_ACTION_CHOICES = (
        EmailAction(NOOP, _('noop')),
        EmailAction(REPLACE_PRIMARY, _('replace primary email')),
    )

    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name=_('email'))
    primary = models.BooleanField(
        default=False,
        help_text=_('The primary address receives all account notifications.'),
        verbose_name=_('is primary'))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='email_addresses',
        related_query_name='email_address',
        verbose_name=_('user'))
    verified = models.BooleanField(
        default=False,
        verbose_name=_('verified'))
    verified_action = models.PositiveSmallIntegerField(
        choices=VERIFIED_ACTION_CHOICES,
        default=NOOP,
        help_text=_('The action to perform after the email is verified.'),
        verbose_name=_('verified action'))

    objects = managers.EmailAddressManager()

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

    def get_absolute_url(self):
        """
        Get the URL of the instance's detail view.

        Returns:
            str:
                The absolute URL of the instance's detail view.
        """
        return reverse('account:email-detail', kwargs={'pk': self.pk})

    def has_object_read_permission(self, request):
        """
        Determine read permissions on the instance for a request.

        Args:
            request:
                The request to get permissions for.

        Returns:
            bool:
                ``True`` if the requesting user owns the email address
                and ``False`` otherwise.
        """
        return request.user == self.user

    def has_object_write_permission(self, request):
        """
        Determine write permissions on the instance for a request.

        Args:
            request:
                The request to get permissions for.

        Returns:
            bool:
                ``True`` if the requesting user owns the email address
                and ``False`` otherwise.
        """
        return request.user == self.user

    def set_primary(self):
        """
        Set this instance as the user's primary email address.

        All other email addresses owned by the user will have
        ``primary`` set to ``False``, and the user's ``email`` attribute
        will be set to this email address.
        """
        self.user.email_addresses.filter(primary=True).update(primary=False)

        self.primary = True
        self.save()

        self.user.email = self.email
        self.user.save()

    def verify(self):
        """
        Mark the email address and perform any additional actions.

        If the action given in the instance's ``verified_action`` field
        is actionable, it is performed.
        """
        self.verified = True
        self.save()

        if self.verified_action == self.REPLACE_PRIMARY:
            old_primary = self.user.email_addresses.get(primary=True)
            self.set_primary()
            old_primary.delete()

            logger.info(
                'Replaced primary email %s with %s for %s',
                old_primary.email,
                self.email,
                self.user.get_full_name())


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
    email = models.ForeignKey(
        'account.EmailAddress',
        null=True,
        related_name='confirmations',
        related_query_name='confirmation',
        verbose_name=_('email'))
    key = models.CharField(
        max_length=settings.EMAIL_CONFIRMATION_KEY_LENGTH,
        unique=True,
        verbose_name=_('key'))

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
                'email': self.email.email,
            })

    def confirm(self):
        """
        Confirm that the associated email is valid.

        This method sets the associated email as verified, and then
        deletes the confirmation.
        """
        self.email.verify()
        self.delete()

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
            'user': self.email.user,
        }
        text_content = render_to_string(
            'account/email/confirm-email.txt',
            context)

        mail.send_mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            message=text_content,
            recipient_list=[self.email.email],
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
