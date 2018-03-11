"""Models for the Know Me app.
"""

import logging

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from rest_email_auth.models import EmailAddress

from rest_framework.reverse import reverse

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
        try:
            user = EmailAddress.objects.get(
                email=email,
                is_verified=True).user
        except EmailAddress.DoesNotExist:
            user = None

        accessor = KMUserAccessor.objects.create(
            email=email,
            is_admin=is_admin,
            km_user=self,
            user_with_access=user)

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
