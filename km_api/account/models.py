"""Models for the ``account`` module.
"""

from collections import namedtuple
import datetime
import logging

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext, ugettext_lazy as _

from rest_framework.reverse import reverse

from permission_utils import model_mixins as mixins

from account import managers
import templated_email


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

        templated_email.send_email(
            context=context,
            subject=_('Please Confirm Your Know Me Email'),
            template='account/email/confirm-email',
            to=self.email.email)


class PasswordReset(models.Model):
    """
    A token allowing a user to reset their password.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at'))
    key = models.CharField(
        max_length=settings.PASSWORD_RESET_KEY_LENGTH,
        unique=True,
        verbose_name=_('key'))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='password_resets',
        related_query_name='password_reset',
        verbose_name=_('user'))

    objects = managers.PasswordResetManager()

    @classmethod
    def create_and_send(cls, email):
        """
        Create a password reset and send it to the user.

        The email is only sent if there is verified email matching the
        provided address present in the database.

        Args:
            email (str):
                The email address to send the password reset to.

        Returns:
            The created password reset.
        """
        try:
            email_instance = EmailAddress.objects.get(
                email=email,
                verified=True)
        except EmailAddress.DoesNotExist:
            logger.warn(
                'Attempted to reset password for unverified email address: %s',
                email)
            return None

        reset = cls.objects.create(user=email_instance.user)
        reset.send_reset(email)

        return reset

    def __str__(self):
        """
        Get a string containing information about the instance.

        Returns:
            str:
                A string containing the user that the reset is for.
        """
        return 'Password reset for {user}'.format(user=self.user)

    def is_expired(self):
        """
        Determine if the instance has expired.

        The duration a password reset is valid for is specified in the
        ``PASSWORD_RESET_EXPIRATION_HOURS`` setting.

        Returns:
            bool:
                ``True`` if the password is expired and ``False``
                otherwise.
        """
        expiration = self.created_at + datetime.timedelta(
            hours=settings.PASSWORD_RESET_EXPIRATION_HOURS)

        return timezone.now() > expiration

    def send_reset(self, email):
        """
        Send the instance's reset email.

        Args:
            email (str):
                The email address to send the password reset to.
        """
        context = {
            'reset_link': settings.PASSWORD_RESET_LINK_TEMPLATE.format(
                key=self.key),
            'user': self.user,
        }

        templated_email.send_email(
            context=context,
            subject=_('Instructions to Reset Your Know Me Password'),
            template='account/email/reset-password',
            to=email)

        logger.info('Sent password reset to %s', email)


class User(PermissionsMixin, AbstractBaseUser):
    """
    A user's profile.

    Attributes:
        created_at (datetime):
            Autogenerated field that stores the time of the user's
            creation.
        email (str):
            The user's primary email address. This is updated when an
            EmailAddress is marked as the primary address.
        is_active (bool):
            Inactive users are not able to log in.
        is_pending (bool):
            A pending user is one that is automatically created. When a
            user signs up with the email attached to a pending user, the
            account is 'finalized'.
        is_staff (bool):
            Staff users are allowed to log in to the admin site.
        is_superuser (bool):
            Superusers have all permissions without them being
            explicitly granted.
        first_name (str):
            The user's first name.
        last_name (str):
            The user's last name.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at'))
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name=_('email'))
    is_active = models.BooleanField(
        default=True,
        help_text=_('Inactive users are not able to log in.'),
        verbose_name=_('is active'))
    is_pending = models.BooleanField(
        default=False,
        help_text=_('A pending user holds placeholder information until a '
                    'user registers with the email address of the pending '
                    'user.'),
        verbose_name=('is pending'))
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

    @classmethod
    def create_pending(cls, email):
        """
        Create a pending user.

        The pending user is a placeholder until a user with the same
        email registers. At that point, the pending user's information
        will be merged with the information given by the registering
        user.

        Args:
            email (str):
                The email address to give the user.

        Returns:
            The newly created pending user.
        """
        return cls.objects.create_user(
            email=email,
            first_name='Pending',
            is_pending=True,
            last_name='User',
            password=None)

    def confirm_pending(self, first_name, last_name, password):
        """
        Confirm a pending user's account.

        This marks the user as 'no longer pending' and merges the
        existing information with the data provided when the user
        registered.
        """
        assert self.is_pending, (
            "'confirm_pending' may only be called on users with "
            "'is_pending = True'.")

        self.first_name = first_name
        self.last_name = last_name
        self.is_pending = False

        self.set_password(password)

        self.save()

        logger.info('Confirmed pending user with email: %s', self.email)

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
        context = {'user': self}

        templated_email.send_email(
            context=context,
            subject=_('Your Know Me Password was Changed'),
            template='account/email/password-changed',
            to=self.email)
