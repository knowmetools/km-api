"""Models for the Know Me app.
"""

import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

import email_utils

from rest_email_auth.models import EmailAddress

from rest_framework.reverse import reverse

from solo.models import SingletonModel

from permission_utils import model_mixins as mixins


logger = logging.getLogger(__name__)


def get_km_user_image_upload_path(km_user, imagename):
    """
    Get the path to upload the kmuser image to.

    Args:
        km_user:
            The km_user whose image is being uploaded.
        imagename (str):
            The original name of the image being uploaded.

    Returns:
        str:
            The original image filename prefixed with
            `users/<user_id>/{file}`.
    """
    return 'know-me/users/{id}/images/{file}'.format(
            file=imagename,
            id=km_user.id)


class Config(SingletonModel):
    """
    Configuration for the Know Me app.

    This model is a singleton for holding variables global to the Know
    Me app.
    """
    minimum_app_version_ios = models.CharField(
        blank=True,
        help_text=_('The minimum version of the iOS app that is usable '
                    'without a required update.'),
        max_length=31)

    class Meta:
        verbose_name = _('config')

    @staticmethod
    def has_read_permission(request):
        """
        Grant all users read permission to the config object.

        Returns:
            ``True``
        """
        return True

    @staticmethod
    def has_write_permission(request):
        """
        Check write permissions on the config object for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            ``True`` if the requesting user is staff and ``False``
            otherwise.
        """
        return request.user.is_staff

    def __str__(self):
        """
        Get a string representation of the instance.

        Returns:
            The string 'Config'.
        """
        return 'Config'


class KMUser(mixins.IsAuthenticatedMixin, models.Model):
    """
    A KMUser tracks information associated with each user of the
    Know Me app.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_('The time that the Know Me user was created.'),
        verbose_name=_('created at'))
    image = models.ImageField(
        blank=True,
        help_text=_("The image to use as the user's hero image."),
        max_length=255,
        null=True,
        upload_to=get_km_user_image_upload_path,
        verbose_name=_('image'))
    is_legacy_user = models.BooleanField(
        default=False,
        help_text=_('A boolean indicating if the user used a prior version of '
                    'Know Me.'),
        verbose_name=_('is legacy user'))
    quote = models.TextField(
        blank=True,
        help_text=_("A quote to introduce the user."),
        null=True,
        verbose_name=_('quote'))
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_('The time that the Know Me user was last updated.'),
        verbose_name=_('updated at'))
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        help_text=_('The user who owns the Know Me app account.'),
        on_delete=models.CASCADE,
        related_name='km_user',
        verbose_name=_('user'))

    class Meta:
        verbose_name = _('Know Me user')
        verbose_name_plural = _('Know Me users')

    def __str__(self):
        """
        Get a string representation of the KMUser.

        Returns:
            str:
                The KMUser's name.
        """
        return self.user.get_short_name()

    @property
    def name(self):
        """
        str:
            The parent user's name.
        """
        return self.user.get_short_name()

    def get_absolute_url(self):
        """
        Get the absolute URL of the instance's detail view.

        Returns:
            str:
                The absolute URL of the instance's detail view.
        """
        return reverse('know-me:km-user-detail', kwargs={'pk': self.pk})

    def get_media_resource_category_list_url(self, request=None):
        """
        Get the absolute URL of the instance's media resource category
        list view.

        Args:
            request (optional):
                A request used as context when constructing the URL. If
                given, the resulting URL will be a full URI with a
                protocol and domain name.

        Returns:
            str:
                The absolute URL of the instance's media resource
                category list view.
        """
        return reverse(
            'know-me:profile:media-resource-category-list',
            kwargs={'pk': self.pk},
            request=request)

    def get_media_resource_list_url(self):
        """
        Get the absolute URL of the instance's media resource list view.

        Returns:
            The URL of the instance's media resource list view.
        """
        return reverse(
            'know-me:profile:media-resource-list',
            kwargs={'pk': self.pk})

    def get_profile_list_url(self, request=None):
        """
        Get the absolute URL of the instance's profile list view.

        Args:
            request (optional):
                A request used as context when constructing the URL. If
                given, the resulting URL will be a full URI with a
                protocol and domain name.

        Returns:
            str:
                The absolute URL of the instance's profile list view.
        """
        return reverse(
            'know-me:profile:profile-list',
            kwargs={'pk': self.pk},
            request=request)

    def has_object_read_permission(self, request):
        """
        Check read permissions on the instance for a request.

        Users have read access if they are the owner of the Know Me user
        or have been granted access through an accessor.

        Args:
            request:
                The request to check permissions for.

        Returns:
            A boolean indicating if the requesting user has read access
            to the instance.
        """
        if request.user == self.user:
            return True

        return self.km_user_accessors.filter(
            is_accepted=True,
            user_with_access=request.user).exists()

    def has_object_write_permission(self, request):
        """
        Check write permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                ``True`` if the requesting user owns the km_user and
                ``False`` otherwise.
        """
        if request.user == self.user:
            return True

        return self.km_user_accessors.filter(
            is_accepted=True,
            is_admin=True,
            user_with_access=request.user).exists()

    def share(self, email, is_admin=False):
        """
        Share a Know Me account with another user.

        Args:
            email (str):
                The email address of the user to share with.
            is_admin (bool):
                A boolean indicating if the invited user has write
                access for profiles and access to private profiles.

        Returns:
            The created ``KMUserAccessor`` instance.
        """
        if self.km_user_accessors.filter(email=email).exists():
            raise ValidationError(
                _('%s has already been invited to view your profiles.') % (
                    email,
                ))

        try:
            user = EmailAddress.objects.get(
                email=email,
                is_verified=True).user
        except EmailAddress.DoesNotExist:
            user = None

        if user is not None:
            if user == self.user:
                raise ValidationError(
                    _('You may not share your own user with yourself.'),
                )

            if self.km_user_accessors.filter(user_with_access=user):
                raise ValidationError(
                    _('That user already has access through a different email '
                      'address.'))

        accessor = KMUserAccessor.objects.create(
            email=email,
            is_admin=is_admin,
            km_user=self,
            user_with_access=user)
        accessor.send_invite()

        logger.info(
            'Shared Know Me user %s (ID %d) with %s',
            self.name,
            self.id,
            email)

        return accessor


class KMUserAccessor(mixins.IsAuthenticatedMixin, models.Model):
    """
    Model to store KMUser access information.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_('The time that the accessor was created.'),
        verbose_name=_('created at'))
    email = models.EmailField(
        help_text=_('The email address used to invite the user.'),
        verbose_name=_('email'))
    is_accepted = models.BooleanField(
        default=False,
        help_text=_('The KMUser has accepted the access.'),
        verbose_name=_('is accepted'))
    is_admin = models.BooleanField(
        default=False,
        help_text=_('A boolean indicating if the user has admin access.'),
        verbose_name=_('is admin'))
    km_user = models.ForeignKey(
        'know_me.KMUser',
        help_text=_('The Know Me user this accessor grants access to.'),
        on_delete=models.CASCADE,
        related_name='km_user_accessors',
        related_query_name='km_user_accessor',
        verbose_name=_('Know Me user'))
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_('The time that the accessor was last updated.'),
        verbose_name=_('updated at'))
    user_with_access = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
        related_name='km_user_accessors',
        related_query_name='km_user_accessor',
        verbose_name=_('user'))

    class Meta(object):
        unique_together = ('km_user', 'user_with_access')
        verbose_name = _('Know Me user accessor')
        verbose_name_plural = _('Know Me user accessors')

    def __str__(self):
        """
        Get a string representation of the KMUserAccessor.

        Returns:
            str:
                A string stating which Know Me user the instance gives
                access to.
        """
        return 'Accessor for {user}'.format(user=self.km_user.name)

    @property
    def accept_url(self):
        """
        The absolute URL of the accessor's accept view.
        """
        return reverse('know-me:accessor-accept', kwargs={'pk': self.pk})

    def get_absolute_url(self, request=None):
        """
        Get the URL of the instance's detail view.

        Args:
            request:
                The request to use as context when constructing the URL.
                Defaults to ``None``.

        Returns:
            The URL of the instance's detail view. If a request is
            provided, a full URL including the protocol and domain will
            be returned. Otherwise a path relative to the root of the
            current domain is returned.
        """
        return reverse(
            'know-me:accessor-detail',
            kwargs={'pk': self.pk},
            request=request)

    def has_object_accept_permission(self, request):
        """
        Check if the requesting user can accept the accessor.

        Only the user granted access through the accessor can accept it.

        Args:
            request:
                The request to check permissions for.

        Returns:
            A boolean indicating if the request user has permission to
            accept the accessor.
        """
        return request.user == self.user_with_access

    def has_object_destroy_permission(self, request):
        """
        Check if the requesting user can destroy the accessor.

        Args:
            request:
                The request to check permissions for.

        Returns:
            A boolean indicating if the requesting user has permission
            to destroy the accessor.
        """
        return request.user in [self.km_user.user, self.user_with_access]

    def has_object_read_permission(self, request):
        """
        Check read permissions on the instance for a request.

        Users have read access if they are the owner of the Know Me user
        or have been granted access through an accessor.

        Args:
            request:
                The request to check permissions for.

        Returns:
            A boolean indicating if the requesting user has read access
            to the instance.
        """
        return request.user in [self.km_user.user, self.user_with_access]

    def has_object_write_permission(self, request):
        """
        Check write permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            A boolean indicating if the requesting user has write access
            to the instance.
        """
        return request.user == self.km_user.user

    def send_invite(self):
        """
        Send a notification email about the invite.
        """
        context = {
            'name': self.km_user.name,
        }

        email_utils.send_email(
            context=context,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email],
            subject=_('You Have Been Invited to Follow Someone on Know Me'),
            template_name='know_me/emails/invite',
        )

        logger.info(
            'Sent follow invitation to %s',
            self.email,
        )


class LegacyUser(models.Model):
    """
    Model to track legacy users.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_('The time the legacy user was created.'),
        verbose_name=_('created at'))
    email = models.EmailField(
        help_text=_("The user's email address."),
        max_length=255,
        unique=True,
        verbose_name=_('email'))
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_('The time the legacy user was last updated.'),
        verbose_name=_('updated at'))

    class Meta:
        ordering = ('email',)
        verbose_name = _('legacy user')
        verbose_name_plural = _('legacy users')

    def __str__(self):
        """
        Get a string representation of the instance.

        Returns:
            The instance's email.
        """
        return self.email

    @staticmethod
    def has_read_permission(request):
        """
        Determine if the requesting user has read permissions for legacy
        users.

        Only staff should have this permission.

        Returns:
            A boolean indicating if the requesting user should be
            granted read access to legacy users.
        """
        return request.user.is_staff

    @staticmethod
    def has_write_permission(request):
        """
        Determine if the requesting user has write permissions for
        legacy users.

        Only staff should have this permission.

        Returns:
            A boolean indicating if the requesting user should be
            granted write access to legacy users.
        """
        return request.user.is_staff

    def get_absolute_url(self):
        """
        Get the URL of the instance's detail view.

        Returns:
            The absolute URL of the instance's detail view.
        """
        return reverse('know-me:legacy-user-detail', kwargs={'pk': self.pk})


class Subscription(mixins.IsAuthenticatedMixin, models.Model):
    """
    A subscription to Know Me.
    """
    is_active = models.BooleanField(
        help_text=_('A boolean indicating if the subscription is active.'),
        verbose_name=_('is active'),
    )
    time_created = models.DateTimeField(
        auto_now_add=True,
        help_text=_('The time that the subscription instance was created.'),
        verbose_name=_('creation time'),
    )
    time_updated = models.DateTimeField(
        auto_now=True,
        help_text=_("The time of the subscription's last update."),
        verbose_name=_('last update time'),
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        help_text=_('The user who has a Know Me subscription'),
        on_delete=models.CASCADE,
        related_name='know_me_subscription',
        verbose_name=_('user'),
    )

    class Meta:
        ordering = ('time_created',)
        verbose_name = _('Know Me subscription')
        verbose_name_plural = _('Know Me subscriptions')

    def __str__(self):
        """
        Get a user readable string representation of the instance.

        Returns:
            A string containing the name of the user who owns the
            subscription.
        """
        return 'Know Me subscription for {user}'.format(
            user=self.user.get_full_name(),
        )


class SubscriptionAppleData(mixins.IsAuthenticatedMixin, models.Model):
    """
    Data related to a subscription through Apple.
    """
    receipt_data = models.TextField(
        help_text=_('The receipt data that is base 64 encoded.'),
        verbose_name=_('receipt data'),
    )
    subscription = models.OneToOneField(
        'know_me.Subscription',
        help_text=_('The Know Me subscription the data belongs to.'),
        on_delete=models.CASCADE,
        related_name='apple_data',
        verbose_name=_('subscription'),
    )
    time_created = models.DateTimeField(
        auto_now_add=True,
        help_text=_(
            'The time that the Apple subscription was initially recorded.',
        ),
        verbose_name=_('creation time'),
    )
    time_updated = models.DateTimeField(
        auto_now=True,
        help_text=_("The time of the subscription's last update."),
        verbose_name=_('last update time'),
    )

    class Meta:
        ordering = ('time_created',)
        verbose_name = _('Apple subscription')
        verbose_name_plural = _('Apple subscriptions')

    def __str__(self):
        """
        Get a user readable string describing the instance.

        Returns:
            A string containing information about the parent
            subscription.
        """
        return 'Apple subscription data for the {subscription}'.format(
            subscription=self.subscription,
        )

    def has_object_read_permission(self, request):
        """
        Check if the requesting user has read permissions on the
        instance.

        Args:
            request:
                The request to check permissions for.

        Returns:
            A boolean indicating if the requesting user has read
            permissions to the instance.
        """
        return request.user == self.subscription.user

    def has_object_write_permission(self, request):
        """
        Check if the requesting user has write permissions on the
        instance.

        Args:
            request:
                The request to check permissions for.

        Returns:
            A boolean indicating if the requesting user has write
            permissions to the instance.
        """
        return request.user == self.subscription.user
