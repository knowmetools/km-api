"""Models for the Know Me app.
"""

import logging

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

from rest_framework.reverse import reverse

from account.models import EmailAddress
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
            ``km_user/<id>/gallery/``.
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


class EmergencyContact(mixins.IsAuthenticatedMixin, models.Model):
    """
    An emergency contact holds contact information for emergency situations

    Attributes:
        km_user:
            Emergency Contacts parent ``KMUser``.
        name (str):
            The emergency contact's name.
        relation (str):
            Emergency contact's relationship with the profile owner.
        phone_number (big int):
            The emergency contacts phone number.
        alt_phone_number (optional):
            Second optional phone number for the emergency contact.
        email (optional):
            The emergency contact's email address.
    """
    km_user = models.ForeignKey(
        'know_me.KMUser',
        related_name='emergency_contacts',
        related_query_name='emergency_contact',
        verbose_name=_('know me user'))
    name = models.CharField(
        max_length=255,
        verbose_name=_('name'))
    relation = models.CharField(
        max_length=255,
        verbose_name=_('relation'))
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(regex='^1?\d{9,15}$',
                           message='Enter valid phone number',
                           code='invalid_phone_number'), ],
        verbose_name=_('phone number'))
    alt_phone_number = models.CharField(
        blank=True,
        max_length=15,
        validators=[
            RegexValidator(regex='^1?\d{9,15}$',
                           message='Enter valid phone number',
                           code='invalid_phone_number'), ],
        verbose_name=_('alternate phone number'))
    email = models.EmailField(
        blank=True,
        default='',
        verbose_name=_('email'))

    class Meta:
        verbose_name = _('emergency contact')
        verbose_name_plural = _('emergency contact')

    def __str__(self):
        """
        Get a string representation of the emergency contact.

        Returns:
            str:
                The emergency contact's name.
        """
        return self.name

    def get_absolute_url(self):
        """
        Get the URL of the profile item's detail view.

        Returns:
            str:
                The absolute URL of the profile item's detail view.
        """
        return reverse(
            'know-me:emergency-contact-detail',
            kwargs={'pk': self.pk})

    def has_object_read_permission(self, request):
        """
        Check read permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                ``True`` if the requesting user has reads permissions for the
                profile and ``False`` otherwise.
        """
        return self.km_user.has_object_read_permission(request)

    def has_object_write_permission(self, request):
        """
        Check write permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                ``True`` if the requesting user has write permissions for the
                profile and ``False`` otherwise.
        """
        return self.km_user.has_object_write_permission(request)


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

    def get_absolute_url(self):
        """
        Get the URL of the instance's detail view.

        Returns:
            str:
                The absolute URL of the instance's detail view.
        """
        return reverse('know-me:emergency-item-detail', kwargs={'pk': self.pk})

    def has_object_read_permission(self, request):
        """
        Check read permissions on the instance for a request.

        This check is actually performed by the instance's parent
        :class:`.KMUser`.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                A boolean indicating if the request should have read
                permissions for the instance.
        """
        return self.km_user.has_object_read_permission(request)

    def has_object_write_permission(self, request):
        """
        Check write permissions on the instance for a request.

        This check is actually performed by the instance's parent
        :class:`.KMUser`.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                A boolean indicating if the request should have write
                permissions for the instance.
        """
        return self.km_user.has_object_write_permission(request)


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

    def get_emergency_contact_list_url(self, request=None):
        """
        Get the absolute URL of the instance's emergency contact list view.

        Args:
            request (optional):
                A request used as context when constructing the URL. If
                given, the resulting URL will be a full URI with a
                protocol and domain name.

        Returns:
            str:
                The absolute URL of the instance's emeregency contact list
                view.
        """
        return reverse(
            'know-me:emergency-contact-list',
            kwargs={'pk': self.pk},
            request=request)

    def get_emergency_item_list_url(self, request=None):
        """
        Get the URL of the instance's emergency item list.

        Args:
            request (:class:`django.http.HttpRequest`, optional):
                The request to use as context when constructing the URL.

        Returns:
            str:
                The URL of the instance's emergency item list view. If
                ``request`` is not ``None``, the URL will include a
                protocol and domain, otherwise it will be an absolute
                URL.
        """
        return reverse(
            'know-me:emergency-item-list',
            kwargs={'pk': self.pk},
            request=request)

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
                verified=True).user
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
        null=True,
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

    Attributes:
        name:
            The name of the item.
        km_user:
            The km_user that the item is attached to.
        file:
            A file containing some sort of content.
    """
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


class Profile(mixins.IsAuthenticatedMixin, models.Model):
    """
    A profile contains a targeted subset of a ``KMUser``.

    Attributes:
        is_default (bool):
            A boolean controlling if the profile is the default for its
            parent km_user.
        is_private (bool):
            This a private profile with admin only access.
        name (str):
            The name of the profile.
        km_user:
            The ``KMUser`` instance the profile belongs to.
    """
    is_default = models.BooleanField(
        default=False,
        help_text=_('The default profile is displayed initially.'),
        verbose_name=_('is default'))
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
