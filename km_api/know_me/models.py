"""Models for the Know Me app.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from rest_framework.reverse import reverse

from permission_utils import model_mixins as mixins


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
            ``profile/<id>/gallery/``.
    """
    return 'profile/{id}/gallery/{file}'.format(
        file=filename,
        id=item.profile.id)


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


class EmergencyItem(mixins.IsAuthenticatedMixin, models.Model):
    """
    An emergency item holds emergency information for a KMUser.

    Attributes:
        description (optional, str):
            The description for the KMUser.
        media_resource (optional):
            A ``Media Resource`` associated with the emergency item.
        km_user:
            The KMUser the item is connected with.
        name:
            The name of the item.
    """
    description = models.TextField(
        blank=True,
        default='',
        verbose_name=_('description'))
    media_resource = models.ForeignKey(
        'know_me.MediaResource',
        blank=True,
        null=True,
        related_name='emergency_items',
        related_query_name='emergency_item',
        verbose_name=_('media resource'))
    km_user = models.ForeignKey(
        'know_me.KMUser',
        related_name='emergency_items',
        related_query_name='emergency_item',
        verbose_name=_('know me user'))
    name = models.CharField(
        max_length=255,
        verbose_name=_('name'))

    class Meta:
        verbose_name = _('emergency item')
        verbose_name_plural = _('emergency items')

    def __str__(self):
        """
        Get a string representation of the emergency item.

        Returns:
            str:
                The emergency item's name.
        """
        return self.name


class MediaResource(mixins.IsAuthenticatedMixin, models.Model):
    """
    A media resource is an uploaded file attached to a profile.

    Attributes:
        name:
            The name of the item.
        profile:
            The profile that the item is attached to.
        file:
            A file containing some sort of content.
    """
    name = models.CharField(
        max_length=255,
        verbose_name=_('name'))
    profile = models.ForeignKey(
        'know_me.Profile',
        related_name='media_resources',
        related_query_name='media_resource',
        verbose_name=_('profile'))
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
            The user who owns this profile.
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


class ListContent(models.Model):
    """
    Container for a list attached to a :class:`.ProfileItem` instance.
    """
    profile_item = models.OneToOneField(
        'know_me.ProfileItem',
        on_delete=models.CASCADE,
        related_name='list_content',
        verbose_name=_('profile item'))
    """
    The profile item that the list is attached to.
    """

    class Meta(object):
        verbose_name = _('profile item list')
        verbose_name_plural = _('profile item lists')

    def __str__(self):
        """
        Get a string representation of the instance.

        Returns:
            str:
                A string containing information about which profile item
                the list is attached to.
        """
        return "List for profile item '{item}'".format(item=self.profile_item)


class ListEntry(models.Model):
    """
    An entry in a :class:`ListContent` instance.
    """
    list_content = models.ForeignKey(
        'know_me.ListContent',
        on_delete=models.CASCADE,
        related_name='entries',
        related_query_name='entry',
        verbose_name=_('profile item list'))
    """
    The :class:`.ListContent` instance that the entry belongs to.
    """

    text = models.TextField(verbose_name=_('text'))
    """
    str:
        The text that the list entry contains.
    """

    class Meta:
        verbose_name = _('profile item list entry')
        verbose_name_plural = _('profile item list entry')

    def __str__(self):
        """
        Get a string representation of the instance.

        Returns:
            str:
                The list entry's text truncated to 50 characters.
        """
        if len(self.text) > 50:
            return '{}...'.format(self.text[:47])

        return self.text


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
        return reverse('know-me:profile-detail', kwargs={'pk': self.pk})

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
            kwargs={'pk': self.pk},
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
        return reverse('know-me:profile-group-detail', kwargs={'pk': self.pk})

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
        null=True,
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
                ``True`` if the requesting user owns the profile the
                instance belongs to and ``False`` otherwise.
        """
        return request.user == self.topic.group.profile.user

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
        return request.user == self.topic.group.profile.user


class ProfileTopic(mixins.IsAuthenticatedMixin, models.Model):
    """
    A profile topic holds a category of information for a profile group.

    Attributes:
        group:
            The topic's parent ``ProfileGroup``.
        name (str):
            The topic's name.
    """
    GROUPED = 1
    PAGED = 2
    TEXT = 3
    VISUAL = 4

    TOPIC_TYPE_CHOICES = (
        (GROUPED, _('grouped topic')),
        (PAGED, _('paged topic')),
        (TEXT, _('text topic')),
        (VISUAL, _('visual topic')),
    )

    group = models.ForeignKey(
        'know_me.ProfileGroup',
        on_delete=models.CASCADE,
        related_name='topics',
        related_query_name='topic',
        verbose_name=_('profile group'))
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
