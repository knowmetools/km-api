"""Models for the Know Me app.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from rest_framework.reverse import reverse

from know_me.models import mixins


def get_gallery_item_upload_path(item, filename):
    """
    Get the path to upload a gallery item's resource to.

    Args:
        item:
            The gallery item whose resource is being uploaded.
        filename (str):
            The original name of the file being uploaded.

    Returns:
        str:
            The original filename prefixed with
            ``profile/<id>/gallery/``.
    """
    return 'profile/{id}/gallery/{file}'.format(
        file=filename,
        id=item.profile.id)


class GalleryItem(mixins.IsAuthenticatedMixin, models.Model):
    """
    A gallery item is an uploaded file attached to a profile.

    Attributes:
        name:
            The name of the item.
        profile:
            The profile that the item is attached to.
        resource:
            A file containing some sort of content.
    """
    name = models.CharField(
        max_length=255,
        verbose_name=_('name'))
    profile = models.ForeignKey(
        'know_me.Profile',
        related_name='gallery_items',
        related_query_name='gallery_item',
        verbose_name=_('profile'))
    resource = models.FileField(
        max_length=255,
        upload_to=get_gallery_item_upload_path,
        verbose_name=_('resource'))

    class Meta:
        verbose_name = _('gallery item')
        verbose_name_plural = _('gallery items')

    def __str__(self):
        """
        Get a string representation of the gallery item.

        Returns:
            str:
                The gallery item's name.
        """
        return self.name

    def get_absolute_url(self):
        """
        Get the URL of the instance's detail view.

        Returns:
            str:
                The absolute URL of the instance's detail view.
        """
        return reverse(
            'know-me:gallery-item-detail',
            kwargs={
                'gallery_item_pk': self.pk,
                'profile_pk': self.profile.pk,
            })

    def has_object_read_permission(self, request):
        """
        Check read permissions on the instance for a given request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                ``True`` if the request is allowed to read the instance
                and ``False`` otherwise.
        """
        return self.profile.user == request.user

    def has_object_write_permission(self, request):
        """
        Check write permissions on the instance for a given request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                ``True`` if the request is allowed to write to the
                instance and ``False`` otherwise.
        """
        return self.profile.user == request.user


class Profile(mixins.IsAuthenticatedMixin, models.Model):
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

    def get_gallery_url(self, request=None):
        """
        Get the absolute URL of the instance's gallery view.

        Args:
            request (optional):
                A request used as context when constructing the URL. If
                given, the resulting URL will be a full URI with a
                protocol and domain name.

        Returns:
            str:
                The absolute URL of the instance's gallery view.
        """
        return reverse(
            'know-me:gallery',
            kwargs={'profile_pk': self.pk},
            request=request)

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

    def has_object_read_permission(self, request):
        """
        Check read permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                ``True`` if the requesting user owns the profile and
                ``False`` otherwise.
        """
        return request.user == self.user

    def has_object_write_permission(self, request):
        """
        Check write permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                ``True`` if the requesting user owns the profile and
                ``False`` otherwise.
        """
        return request.user == self.user


class ProfileGroup(mixins.IsAuthenticatedMixin, models.Model):
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

    def get_row_list_url(self, request=None):
        """
        Get the URL of the instance's row list view.

        Args:
            request (optional):
                The request to use when constructing the URL. If a
                request is provided, the URL will include a protocol
                and domain. Otherwise it will be an absolute URL.

        Returns:
            str:
                The URL of the instance's row list view.
        """
        return reverse(
            'know-me:profile-row-list',
            kwargs={
                'group_pk': self.pk,
                'profile_pk': self.profile.pk,
            },
            request=request)

    def has_object_read_permission(self, request):
        """
        Check read permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                ``True`` if the requesting user owns the group's parent
                profile and ``False`` otherwise.
        """
        return request.user == self.profile.user

    def has_object_write_permission(self, request):
        """
        Check write permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                ``True`` if the requesting user owns the group's parent
                profile and ``False`` otherwise.
        """
        return request.user == self.profile.user


class ProfileItem(mixins.IsAuthenticatedMixin, models.Model):
    """
    A profile item holds a piece of information for a profile row.

    Attributes:
        gallery_item (optional):
            A ``GalleryItem`` associated with the profile item.
        name (str);
            The item's name.
        row:
            The profile row the item is part of.
        text (optional):
            The item's text. Defaults to an empty string.
    """
    gallery_item = models.ForeignKey(
        'know_me.GalleryItem',
        blank=True,
        null=True,
        related_name='profile_items',
        related_query_name='profile_item',
        verbose_name=_('gallery item'))
    name = models.CharField(
        max_length=255,
        verbose_name=_('name'))
    row = models.ForeignKey(
        'know_me.ProfileRow',
        related_name='items',
        related_query_name='item',
        verbose_name=_('profile row'))
    text = models.TextField(
        blank=True,
        default='',
        verbose_name=_('text'))

    class Meta:
        verbose_name = _('profile item')
        verbose_name_plural = _('profile items')

    def __str__(self):
        """
        Get a string representation of the profile item.

        Returns:
            str:
                The profile item's name.
        """
        return self.name

    def get_absolute_url(self):
        """
        Get the URL of the profile item's detail view.

        Returns:
            str:
                The absolute URL of the profile item's detail view.
        """
        return reverse('know-me:profile-item-detail', kwargs={'pk': self.pk})

    def has_object_read_permission(self, request):
        """
        Check read permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                ``True`` if the requesting user owns the profile the
                instance belongs to and ``False`` otherwise.
        """
        return request.user == self.row.group.profile.user

    def has_object_write_permission(self, request):
        """
        Check write permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                ``True`` if the requesting user owns the profile the
                instance belongs to and ``False`` otherwise.
        """
        return request.user == self.row.group.profile.user


class ProfileRow(mixins.IsAuthenticatedMixin, models.Model):
    """
    A profile row holds a category of information for a profile group.

    Attributes:
        group:
            The row's parent ``ProfileGroup``.
        name (str):
            The row's name.
    """
    GROUPED = 1
    PAGED = 2
    TEXT = 3
    VISUAL = 4

    ROW_TYPE_CHOICES = (
        (GROUPED, _('grouped row')),
        (PAGED, _('paged row')),
        (TEXT, _('text row')),
        (VISUAL, _('visual row')),
    )

    group = models.ForeignKey(
        'know_me.ProfileGroup',
        on_delete=models.CASCADE,
        related_name='rows',
        related_query_name='row',
        verbose_name=_('profile group'))
    name = models.CharField(
        max_length=255,
        verbose_name=_('name'))
    row_type = models.PositiveSmallIntegerField(
        choices=ROW_TYPE_CHOICES,
        verbose_name=_('row type'))

    class Meta:
        verbose_name = _('profile row')
        verbose_name_plural = _('profile rows')

    def __str__(self):
        """
        Get a string representation of the profile group.

        Returns:
            str:
                The instance's name.
        """
        return self.name

    def get_absolute_url(self):
        """
        Get the URL of the instance's detail view.

        Returns:
            str:
                The absolute URL of the instance's detail view.
        """
        return reverse('know-me:profile-row-detail', kwargs={'pk': self.pk})

    def get_item_list_url(self, request=None):
        """
        Get the URL of the row's item list view.

        Args:
            request (optional):
                The request to use when constructing the URL. If it is
                provided, the resulting URL will include a protocol and
                domain. Otherwise the resulting URL will be an absolute
                URL (beginning with a ``'/'``). Defaults to ``None``.

        Returns:
            str:
                The URL of the row's item list view.
        """
        return reverse(
            'know-me:profile-item-list',
            kwargs={'pk': self.pk},
            request=request)

    def has_object_read_permission(self, request):
        """
        Check read permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                ``True`` if the requesting user owns the profile the
                instance belongs to and ``False`` otherwise.
        """
        return request.user == self.group.profile.user

    def has_object_write_permission(self, request):
        """
        Check write permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                ``True`` if the requesting user owns the profile the
                instance belongs to and ``False`` otherwise.
        """
        return request.user == self.group.profile.user
