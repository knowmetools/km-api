"""Admin configuration for ``know_me`` module.
"""

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from know_me import models


# Inlines used in other admin objects

class ImageContentInline(admin.StackedInline):
    """
    Inline admin for profile item image content.
    """
    fields = ('image_resource', 'media_resource', 'description')
    model = models.ImageContent


class ListEntryInline(admin.StackedInline):
    """
    Inline admin for list entries.
    """
    extra = 1
    fields = ('text',)
    model = models.ListEntry


# Standard admin objects


@admin.register(models.EmergencyItem)
class EmergencyItemAdmin(admin.ModelAdmin):
    """
    Admin for the ``EmergencyItem`` model.
    """
    fields = ('name', 'km_user', 'media_resource', 'description')
    list_display = ('name', 'km_user')
    search_fields = ('name',)


@admin.register(models.EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    """
    Admin for the ``EmergencyContact`` model.
    """
    fields = (
        'km_user', 'name', 'relation', 'phone_number', 'alt_phone_number',
        'email'
    )
    list_display = ('name', 'km_user')
    search_fields = ('name',)


@admin.register(models.KMUser)
class KMUserAdmin(admin.ModelAdmin):
    """
    Admin for the ``KMUser`` model.
    """
    fields = ('user', 'image', 'quote')
    list_display = ('user',)
    search_fields = ('user__first_name', 'user__last_name')


@admin.register(models.KMUserAccessor)
class KMUserAccessor(admin.ModelAdmin):
    """
    Admin for the ``KMUserAccessor`` model.
    """
    fields = (
        'km_user',
        'user_with_access',
        'accepted',
        'can_write_everywhere')
    list_display = (
        'km_user',
        'user_with_access',
        'accepted',
        'can_write_everywhere')
    search_fields = (
        'km_user__user__first_name',
        'km_user__user__last_name',
        'user_with_access__first_name',
        'user_with_access__last_name')


@admin.register(models.ListContent)
class ListContentAdmin(admin.ModelAdmin):
    """
    Admin for the ``ListContent`` model.
    """
    fields = ('profile_item',)
    inlines = (ListEntryInline,)
    list_display = ('string_repr', 'profile_item')
    search_fields = ('profile_item__name',)

    def string_repr(self, list_content):
        """
        Get the string representation of a ``ListContent`` instance.

        Args:
            list_content (:class:`.ListContent`):
                The list content instance to get a string representation
                of.

        Returns:
            str:
                The string representation of the provided list content.
        """
        return str(list_content)
    string_repr.admin_order_field = 'profile_item__name'
    string_repr.short_description = _('list content')


@admin.register(models.MediaResource)
class MediaResourceAdmin(admin.ModelAdmin):
    """
    Admin for the ``MediaResource`` model.
    """
    fields = ('name', 'km_user', 'file')
    list_display = ('name', 'km_user')
    search_fields = ('name', 'km_user__user__name')


@admin.register(models.ProfileAccessor)
class ProfileAccessorAdmin(admin.ModelAdmin):
    """
    Admin for the ``ProfileAccessor`` model.
    """
    fields = ('km_user_accessor', 'profile', 'can_write')
    list_display = ('profile', 'can_write')
    search_fields = (
        'profile__name',
        'km_user_accessor__user_with_access__first_name',
        'km_user_accessor__user_with_access__last_name')


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin for the ``Profile`` model.
    """
    fields = ('name', 'km_user', 'is_default', 'is_private')
    list_display = ('name', 'km_user', 'is_default', 'is_private')
    list_filter = ('is_default', 'is_private')
    search_fields = ('name', 'km_user__user__name')


@admin.register(models.ProfileItem)
class ProfileItemAdmin(admin.ModelAdmin):
    """
    Admin for the ``ProfileItem`` model.
    """
    inlines = (ImageContentInline,)
    fields = ('name', 'topic')
    list_display = ('name', 'get_km_user', 'get_profile', 'topic')
    search_fields = ('name',)

    def get_profile(self, item):
        """
        Get the profile the profile item belongs to.

        Args:
            item:
                The profile item to get the parent profile of.

        Returns:
            The parent profile of the given profile item.
        """
        return item.topic.profile
    get_profile.admin_order_field = 'topic__profile'
    get_profile.short_description = _('profile')

    def get_km_user(self, item):
        """
        Get the km_user the profile item belongs to.

        Args:
            item:
                The profile item to get the parent km_user of.

        Returns:
            The parent km_user of the given profile item.
        """
        return item.topic.profile.km_user
    get_km_user.admin_order_field = 'topic__profile__km_user'
    get_km_user.short_description = _('km_user')


@admin.register(models.ProfileTopic)
class ProfileTopicAdmin(admin.ModelAdmin):
    """
    Admin for the ``ProfileTopic`` model.
    """
    fields = ('name', 'profile', 'topic_type')
    list_display = ('name', 'profile', 'topic_type')
    list_filter = ('topic_type',)
    search_fields = ('profile__name', 'name')
