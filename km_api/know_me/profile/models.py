from django.db import models
from django.utils.translation import ugettext_lazy as _

from permission_utils import model_mixins as mixins

from rest_framework.reverse import reverse


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
    return "know-me/users/{id}/media-resources/{file}".format(
        file=filename, id=item.km_user.id
    )


def get_profile_item_image_upload_path(item, filename):
    """
    Get the path to upload a profile item's image to.

    Args:
        item:
            The profile item whose image is being uploaded.
        filename:
            The original name of the image being uploaded.

    Returns:
        The path to upload the profile item's image to.
    """
    return "know-me/users/{id}/profile-images/{file}".format(
        file=filename, id=item.topic.profile.km_user.id
    )


class ListEntry(mixins.IsAuthenticatedMixin, models.Model):
    """
    An entry in a list for a profile item.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The time that the list entry was created."),
        verbose_name=_("created at"),
    )
    profile_item = models.ForeignKey(
        "profile.ProfileItem",
        help_text=_("The profile item that the list entry belongs to."),
        on_delete=models.CASCADE,
        related_name="list_entries",
        related_query_name="list_entry",
        verbose_name=_("profile item"),
    )
    text = models.CharField(
        help_text=_("The text associated with the entry."),
        max_length=255,
        verbose_name=_("text"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_("The time that the list entry was last updated."),
        verbose_name=_("updated at"),
    )

    class Meta:
        order_with_respect_to = "profile_item"
        verbose_name = _("profile item list entry")
        verbose_name_plural = _("profile item list entries")

    def __str__(self):
        """
        Get a string representation of the instance.

        Returns:
            The instance's text.
        """
        return self.text

    def get_absolute_url(self):
        """
        Get the URL of the instance's detail view.

        Returns:
            The absolute URL of the instance's detail view.
        """
        return reverse(
            "know-me:profile:list-entry-detail", kwargs={"pk": self.pk}
        )

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
        return self.profile_item.has_object_read_permission(request)

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
        return self.profile_item.has_object_write_permission(request)


class MediaResource(mixins.IsAuthenticatedMixin, models.Model):
    """
    Some form of media file owned by a Know Me user.
    """

    cover_style = models.PositiveSmallIntegerField(
        blank=True,
        default=0,
        help_text=_(
            "An integer that provides a hint for clients as to how to "
            "style the resource."
        ),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The time that the resource was created."),
        verbose_name=_("created at"),
    )
    file = models.FileField(
        blank=True,
        help_text=_("The file to associate with the resource."),
        upload_to=get_media_resource_upload_path,
        verbose_name=_("file"),
    )
    km_user = models.ForeignKey(
        "know_me.KMUser",
        help_text=_("The Know Me user who owns the resource."),
        on_delete=models.CASCADE,
        related_name="media_resources",
        related_query_name="media_resource",
        verbose_name=_("Know Me user"),
    )
    link = models.URLField(
        blank=True,
        help_text=_("A link to an external resource."),
        max_length=255,
        verbose_name=_("link"),
    )
    name = models.CharField(
        help_text=_("The name of the resource."),
        max_length=255,
        verbose_name=_("name"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_("The time that the resource was last updated."),
        verbose_name=_("updated at"),
    )

    class Meta:
        verbose_name = _("media resource")
        verbose_name_plural = _("media resources")

    def __str__(self):
        """
        Get a string representation of the resource.

        Returns:
            The resource's name.
        """
        return self.name

    def get_absolute_url(self):
        """
        Get the URL of the instance's detail view.

        Returns:
            The absolute URL of the instance's detail view.
        """
        return reverse(
            "know-me:profile:media-resource-detail", kwargs={"pk": self.pk}
        )

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
    A profile contains a targeted set of information about a Know Me
    user.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The time that the profile was created."),
        verbose_name=_("created at"),
    )
    is_private = models.BooleanField(
        default=False,
        help_text=_(
            "A boolean indicating if the profile is private. Private "
            "profiles are only visible to team leaders."
        ),
        verbose_name=_("is private"),
    )
    km_user = models.ForeignKey(
        "know_me.KMUser",
        help_text=_("The Know Me user who owns the profile."),
        on_delete=models.CASCADE,
        related_name="profiles",
        related_query_name="profile",
        verbose_name=_("Know Me user"),
    )
    name = models.CharField(
        help_text=_("The name of the profile."),
        max_length=255,
        verbose_name=_("name"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_("The time that the profile was last updated."),
        verbose_name=_("updated at"),
    )

    class Meta:
        order_with_respect_to = "km_user"
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self):
        """
        Get a string representation of the instance.

        Returns:
            The instance's name.
        """
        return self.name

    def get_absolute_url(self):
        """
        Get the URL of the instance's detail view.

        Returns:
            The absolute URL of the instance's detail view.
        """
        return reverse(
            "know-me:profile:profile-detail", kwargs={"pk": self.pk}
        )

    def get_topic_list_url(self):
        """
        Get the URL of the instance's topic list view.

        Returns:
            The absolute URL of the instance's topic list view.
        """
        return reverse(
            "know-me:profile:profile-topic-list", kwargs={"pk": self.pk}
        )

    def has_object_read_permission(self, request):
        """
        Check read permissions on the instance for a request.

        If the profile is private, it requires the requesting user to be
        granted admin permissions (or be the owner). This check is
        already implemented in the write-permissions check of the parent
        Know Me user, so we use it here.

        Args:
            request:
                The request to check permissions for.

        Returns:
            A boolean indicating if the requesting user has read
            permissions on the instance.
        """
        if self.is_private:
            return self.km_user.has_object_write_permission(request)

        return self.km_user.has_object_read_permission(request)

    def has_object_write_permission(self, request):
        """
        Check write permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            A boolean indicating if the requesting user has write
            permissions on the instance.
        """
        return self.km_user.has_object_write_permission(request)


class ProfileItem(mixins.IsAuthenticatedMixin, models.Model):
    """
    A profile item contains a single piece of information for a topic.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The time that the item was created."),
        verbose_name=_("created at"),
    )
    description = models.TextField(
        blank=True,
        help_text=_("A more detailed description of the item's content"),
        verbose_name=_("description"),
    )
    image = models.ImageField(
        blank=True,
        help_text=_("An optional image to attach to the profile item."),
        upload_to=get_profile_item_image_upload_path,
        verbose_name=_("image"),
    )
    media_resource = models.ForeignKey(
        "profile.MediaResource",
        blank=True,
        help_text=_("The optional media resource attached to the item."),
        null=True,
        on_delete=models.SET_NULL,
        related_name="profile_items",
        related_query_name="profile_item",
        verbose_name=_("media resource"),
    )
    name = models.CharField(
        help_text=_("The name of the profile item."),
        max_length=255,
        verbose_name=_("name"),
    )
    topic = models.ForeignKey(
        "profile.ProfileTopic",
        help_text=_("The profile topic that the item belongs to."),
        on_delete=models.CASCADE,
        related_name="items",
        related_query_name="item",
        verbose_name=_("profile topic"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_("The time that the item was last updated."),
        verbose_name=_("updated at"),
    )

    class Meta:
        order_with_respect_to = "topic"
        verbose_name = _("profile item")
        verbose_name_plural = _("profile items")

    def __str__(self):
        """
        Get a string representation of the instance.

        Returns:
            The instance's name.
        """
        return self.name

    def get_absolute_url(self):
        """
        Get the URL of the instance's detail view.

        Returns:
            The absolute URL of the instance's detail view.
        """
        return reverse(
            "know-me:profile:profile-item-detail", kwargs={"pk": self.pk}
        )

    def get_list_entries_url(self):
        """
        Get the URL of the instance's list entry list view.

        Returns:
            The absolute URL of the instance's list entry list view.
        """
        return reverse(
            "know-me:profile:list-entry-list", kwargs={"pk": self.pk}
        )

    def has_object_read_permission(self, request):
        """
        Check read permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            A boolean indicating if the requesting user has read
            permissions on the instance.
        """
        return self.topic.has_object_read_permission(request)

    def has_object_write_permission(self, request):
        """
        Check write permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            A boolean indicating if the requesting user has write
            permissions on the instance.
        """
        return self.topic.has_object_write_permission(request)


class ProfileTopic(mixins.IsAuthenticatedMixin, models.Model):
    """
    A profile topic contains a category of information for a profile.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The time that the topic was created."),
        verbose_name=_("created at"),
    )
    is_detailed = models.BooleanField(
        default=False,
        help_text=_(
            "A boolean indicating if the topic should display its "
            "items' details in the main view."
        ),
        verbose_name=_("is detailed"),
    )
    name = models.CharField(
        help_text=_("The name of the topic."),
        max_length=255,
        verbose_name=_("name"),
    )
    profile = models.ForeignKey(
        "profile.Profile",
        help_text=_("The profile that the topic belongs to."),
        on_delete=models.CASCADE,
        related_name="topics",
        related_query_name="topic",
        verbose_name=_("profile"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_("The time that the profile was last updated."),
        verbose_name=_("updated at"),
    )

    class Meta:
        order_with_respect_to = "profile"
        verbose_name = _("profile topic")
        verbose_name_plural = _("profile topics")

    def __str__(self):
        """
        Get a string representation of the instance.

        Returns:
            The instance's name.
        """
        return self.name

    def get_absolute_url(self):
        """
        Get the URL of the instance's detail view.

        Returns:
            The absolute URL of the instance's detail view.
        """
        return reverse(
            "know-me:profile:profile-topic-detail", kwargs={"pk": self.pk}
        )

    def get_item_list_url(self):
        """
        Get the URL of the instance's item list view.

        Returns:
            The absolute URL of the instance's item list view.
        """
        return reverse(
            "know-me:profile:profile-item-list", kwargs={"pk": self.pk}
        )

    def has_object_read_permission(self, request):
        """
        Check read permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            A boolean indicating if the requesting user has read
            permissions on the instance.
        """
        return self.profile.has_object_read_permission(request)

    def has_object_write_permission(self, request):
        """
        Check write permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            A boolean indicating if the requesting user has write
            permissions on the instance.
        """
        return self.profile.has_object_write_permission(request)
