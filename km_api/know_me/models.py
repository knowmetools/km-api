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


def get_media_resource_upload_path(item, filename):
    """
    Get the path to upload a media resource's file to.

    Args:
        item:
            The media resource whose file is being uploaded.
        filename (str):
            The original name of the file being uploaded.

    Returns:
        str:
            The original filename prefixed with
            ``know-me/users/{id}/media-resources/``.
    """
    return 'know-me/users/{id}/media-resources/{file}'.format(
        file=filename,
        id=item.km_user.id)


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


class ImageContent(models.Model):
    """
    Content for image-type :class:`.ProfileItem` instances.
    """
    description = models.TextField(
        blank=True,
        default='',
        verbose_name=_('description'))
    """
    :obj:`str`, optional:
        Text describing the associated :class:`.ProfileItem`.
    """

    image_resource = models.ForeignKey(
        'know_me.MediaResource',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name=_('image resource'))
    """
    An optional image-type :class:`.MediaResource` instance that
    represents the item's contents.
    """

    media_resource = models.ForeignKey(
        'know_me.MediaResource',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name=_('media resource'))
    """
    An optional additional :class:`.MediaResource` instance associated
    with the item's contents.
    """

    profile_item = models.OneToOneField(
        'know_me.ProfileItem',
        on_delete=models.CASCADE,
        related_name='image_content',
        verbose_name=_('profile item'))
    """
    The :class:`.ProfileItem` instance that the content is attached to.
    """

    class Meta(object):
        verbose_name = _('profile item image content')
        verbose_name_plural = _('profile item image content')

    def has_object_read_permission(self, request):
        """
        Check read permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                ``True`` if the requesting user is allowed to read from
                the instance and ``False`` otherwise.
        """
        return self.profile_item.has_object_read_permission(request)

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
        return self.profile_item.has_object_write_permission(request)

    def __str__(self):
        """
        Get a string representation of the instance.

        Returns:
            str:
                A string indicating which profile item the instance
                belongs to.
        """
        return "Image content for profile item '{item}'".format(
            item=self.profile_item)


class KMUser(mixins.IsAuthenticatedMixin, models.Model):
    """
    A KMUser tracks information associated with each user of the
    Know Me app.

    Attributes:
        user:
            The user who owns this km_user.
        image:
            The user's main image.
        quote (str) :
            A quote from the user.
    """
    image = models.ImageField(
        blank=True,
        max_length=255,
        null=True,
        upload_to=get_km_user_image_upload_path,
        verbose_name=_('image'))
    quote = models.TextField(blank=True, null=True, verbose_name=_('quote'))
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
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
            'know-me:profile-list',
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
                ``True`` if the requesting user owns the km_user and
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
                ``True`` if the requesting user owns the km_user and
                ``False`` otherwise.
        """
        return request.user == self.user

    def share(self, email, can_write=False, has_private_profile_access=False):
        """
        Share a Know Me account with another user.

        Args:
            email (str):
                The email address of the user to share with.
            can_write (bool):
                A boolean indicating if the invited user has write
                access for profiles.
            has_private_profile_access (bool):
                A boolean indicating if the invited user has access to
                profiles marked as private.

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
            can_write=can_write,
            email=email,
            has_private_profile_access=has_private_profile_access,
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

    Attributes:
        accepted (bool):
            A boolean indicating if the share has been accepted yet.
        can_write (bool):
            A boolean indicating if the user has write access to the
            Know Me user's profiles.
        km_user:
            The KMUser sharing access.
        user_with_access:
            The user recieving access.
    """
    accepted = models.BooleanField(
        default=False,
        help_text=_('The KMUser has accepted the access.'),
        verbose_name=_('is accepted'))
    can_write = models.BooleanField(
        default=False,
        help_text=_('Users with write access can make changes to the profiles '
                    'they are invited to.'),
        verbose_name=_('can write'))
    email = models.EmailField(
        help_text=_('The email address used to invite the user.'),
        verbose_name=_('email'))
    has_private_profile_access = models.BooleanField(
        default=False,
        verbose_name=_('has private profile access'))
    km_user = models.ForeignKey(
        'know_me.KMUser',
        null=True,
        related_name='km_user_accessors',
        related_query_name='km_user_accessor',
        verbose_name=_('Know Me user'))
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


class ListContent(mixins.IsAuthenticatedMixin, models.Model):
    """
    Model to store list content for a :class:`.ProfileItem`.
    """
    profile_item = models.OneToOneField(
        'know_me.ProfileItem',
        on_delete=models.CASCADE,
        related_name='list_content',
        verbose_name=_('profile item'))
    """
    :class:`.ProfileItem`:
        The profile item that the list content is attached to.
    """

    class Meta(object):
        verbose_name = _('profile item list content')
        verbose_name_plural = _('profile item list content')

    def get_list_entry_list_url(self, request=None):
        """
        Get the URL of the content's entry list view.

        Args:
            request (optional):
                The request to use when constructing the URL. If it is
                provided, the resulting URL will include a protocol and
                domain. Otherwise the resulting URL will be an absolute
                URL (beginning with a ``'/'``). Defaults to ``None``.

        Returns:
            str:
                The URL of the content's entry list view.
        """
        return reverse(
            'know-me:list-entry-list',
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
                ``True`` if the requesting user is allowed to read from
                the instance and ``False`` otherwise.
        """
        return self.profile_item.has_object_read_permission(request)

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
        return self.profile_item.has_object_write_permission(request)

    def __str__(self):
        """
        Get a string representation of the instance.

        Returns:
            str:
                A message indicating which profile item the list content
                belongs to.
        """
        return "List content for profile item '{item}'".format(
            item=self.profile_item)


class ListEntry(mixins.IsAuthenticatedMixin, models.Model):
    """
    An entry in a list for a specific profile item.
    """
    list_content = models.ForeignKey(
        'know_me.ListContent',
        on_delete=models.CASCADE,
        related_name='entries',
        related_query_name='entry',
        verbose_name=_('list content'))
    """
    :class:`.ListContent`:
        The parent list that the entry is associated with.
    """

    text = models.CharField(
        max_length=255,
        verbose_name=_('text'))
    """
    str:
        Text associated with the list entry.
    """

    class Meta(object):
        verbose_name = _('list entry')
        verbose_name_plural = _('list entries')

    def __str__(self):
        """
        Get a string representation of the instance.

        Returns:
            str:
                The entry's text.
        """
        return self.text

    def get_absolute_url(self):
        """
        Get the URL of the instance's list entry.

        Returns:
            str:
                The absolute URL of the instance's list entry.
        """
        return reverse('know-me:list-entry-detail', kwargs={'pk': self.pk})

    def has_object_read_permission(self, request):
        """
        Check read permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                ``True`` if the requesting user is allowed to read from
                the instance and ``False`` otherwise.
        """
        return self.list_content.has_object_read_permission(request)

    def has_object_write_permission(self, request):
        """
        Check write permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                ``True`` if the requesting user is allowed to write to
                the instance and ``False`` otherwise.
        """
        return self.list_content.has_object_write_permission(request)


class MediaResource(mixins.IsAuthenticatedMixin, models.Model):
    """
    A media resource is an uploaded file attached to a km_user.
    """
    category = models.ForeignKey(
        'know_me.MediaResourceCategory',
        blank=True,
        help_text=_("The category that the resource is a part of."),
        null=True,
        on_delete=models.SET_NULL,
        related_name='media_resources',
        related_query_name='media_resource',
        verbose_name=_('category'))
    name = models.CharField(
        max_length=255,
        verbose_name=_('name'))
    km_user = models.ForeignKey(
        'know_me.KMUser',
        related_name='media_resources',
        related_query_name='media_resource',
        verbose_name=_('km_user'))
    file = models.FileField(
        max_length=255,
        upload_to=get_media_resource_upload_path,
        verbose_name=_('file'))

    class Meta:
        verbose_name = _('media resource')
        verbose_name_plural = _('media resources')

    def __str__(self):
        """
        Get a string representation of the media resource.

        Returns:
            str:
                The media resource's name.
        """
        return self.name

    def get_absolute_url(self):
        """
        Get the URL of the instance's detail view.

        Returns:
            str:
                The absolute URL of the instance's detail view.
        """
        return reverse('know-me:media-resource-detail', kwargs={'pk': self.pk})

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
        return self.km_user.user == request.user

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
        return self.km_user.user == request.user


class MediaResourceCategory(mixins.IsAuthenticatedMixin, models.Model):
    """
    Category that a media resource can be placed in.
    """
    km_user = models.ForeignKey(
        'know_me.KMUser',
        help_text=_("The Know Me user who owns the category."),
        on_delete=models.CASCADE,
        related_name='media_resource_categories',
        related_query_name='media_resource_category',
        verbose_name=_('media resource category'))
    name = models.CharField(
        help_text=_("The category's name."),
        max_length=255,
        verbose_name=_('name'))

    class Meta:
        verbose_name = _('media resource category')
        verbose_name_plural = _('media resource categories')

    def __str__(self):
        """
        Get a string representation of the category.

        Returns:
            The category's name.
        """
        return self.name

    def has_object_read_permission(self, request):
        """
        Check read permissions on the instance for a given request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            The permissions granted by the instance's parent Know Me
            user.
        """
        return self.km_user.has_object_read_permission(request)

    def has_object_write_permission(self, request):
        """
        Check write permissions on the instance for a given request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            The permissions granted by the instance's parent Know Me
            user.
        """
        return self.km_user.has_object_write_permission(request)


class Profile(mixins.IsAuthenticatedMixin, models.Model):
    """
    A profile contains a targeted subset of a ``KMUser``.

    Attributes:
        is_private (bool):
            This a private profile with admin only access.
        name (str):
            The name of the profile.
        km_user:
            The ``KMUser`` instance the profile belongs to.
    """
    is_private = models.BooleanField(
        default=False,
        help_text=_('Private profiles are only visable to admin.'),
        verbose_name=_('is private'))
    km_user = models.ForeignKey(
        'know_me.KMUser',
        null=True,
        on_delete=models.CASCADE,
        related_name='profiles',
        related_query_name='profile',
        verbose_name=_('know me user'))
    name = models.CharField(
        max_length=255,
        verbose_name=_('name'))

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
            The URL of the instance's detail view.
        """
        return reverse('know-me:profile-detail', kwargs={'pk': self.pk})

    def get_topic_list_url(self, request=None):
        """
        Get the URL of the instance's topic list view.

        Args:
            request (optional):
                The request to use when constructing the URL. If a
                request is provided, the URL will include a protocol
                and domain. Otherwise it will be an absolute URL.

        Returns:
            str:
                The URL of the instance's topic list view.
        """
        return reverse(
            'know-me:profile-topic-list',
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
                ``True`` if the requesting user owns the profile's parent
                km_user and ``False`` otherwise.
        """
        return request.user == self.km_user.user

    def has_object_write_permission(self, request):
        """
        Check write permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                ``True`` if the requesting user owns the profile's parent
                km_user and ``False`` otherwise.
        """
        return request.user == self.km_user.user


class ProfileItem(mixins.IsAuthenticatedMixin, models.Model):
    """
    A profile item holds a piece of information for a profile topic.
    """
    name = models.CharField(
        max_length=255,
        verbose_name=_('name'))
    """
    str:
        The profile item's name.
    """

    topic = models.ForeignKey(
        'know_me.ProfileTopic',
        related_name='items',
        related_query_name='item',
        verbose_name=_('profile topic'))
    """
    :class:`.ProfileTopic`:
        The profile topic that the item belongs to.
    """

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
                ``True`` if the requesting user owns the km_user the
                instance belongs to and ``False`` otherwise.
        """
        return request.user == self.topic.profile.km_user.user

    def has_object_write_permission(self, request):
        """
        Check write permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                ``True`` if the requesting user owns the km_user the
                instance belongs to and ``False`` otherwise.
        """
        return request.user == self.topic.profile.km_user.user


class ProfileTopic(mixins.IsAuthenticatedMixin, models.Model):
    """
    A profile topic holds a category of information for a profile.

    Attributes:
        profile:
            The topic's parent ``Profile``.
        name (str):
            The topic's name.
    """
    # The numbering for these fields is augmented due to the previous
    # presence of page and group rows.
    TEXT = 3
    VISUAL = 4

    TOPIC_TYPE_CHOICES = (
        (TEXT, _('text topic')),
        (VISUAL, _('visual topic')),
    )

    profile = models.ForeignKey(
        'know_me.Profile',
        on_delete=models.CASCADE,
        related_name='topics',
        related_query_name='topic',
        verbose_name=_('profile'))
    name = models.CharField(
        max_length=255,
        verbose_name=_('name'))
    topic_type = models.PositiveSmallIntegerField(
        choices=TOPIC_TYPE_CHOICES,
        verbose_name=_('topic type'))

    class Meta:
        verbose_name = _('profile topic')
        verbose_name_plural = _('profile topics')

    def __str__(self):
        """
        Get a string representation of the profile.

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
        return reverse('know-me:profile-topic-detail', kwargs={'pk': self.pk})

    def get_item_list_url(self, request=None):
        """
        Get the URL of the topic's item list view.

        Args:
            request (optional):
                The request to use when constructing the URL. If it is
                provided, the resulting URL will include a protocol and
                domain. Otherwise the resulting URL will be an absolute
                URL (beginning with a ``'/'``). Defaults to ``None``.

        Returns:
            str:
                The URL of the topic's item list view.
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
                ``True`` if the requesting user owns the km_user the
                instance belongs to and ``False`` otherwise.
        """
        return request.user == self.profile.km_user.user

    def has_object_write_permission(self, request):
        """
        Check write permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                ``True`` if the requesting user owns the km_user the
                instance belongs to and ``False`` otherwise.
        """
        return request.user == self.profile.km_user.user
