"""Admin configuration for ``know_me`` module.
"""

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from know_me import models


@admin.register(models.GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    """
    Admin for the ``GalleryItem`` model.
    """
    fields = ('name', 'profile', 'resource')
    list_display = ('name', 'profile')
    search_fields = ('name', 'profile__name')


@admin.register(models.KMUser)
class KMUserAdmin(admin.ModelAdmin):
    """
    Admin for the ``KMUser`` model.
    """
    fields = ('user', 'image', 'quote')
    list_display = ('user',)
    search_fields = ('user__first_name', 'user__last_name')


@admin.register(models.ListContent)
class ListContentAdmin(admin.ModelAdmin):
    """
    Admin for the ``ListContent`` model.
    """
    fields = ('profile_item',)
    list_display = ('profile_item',)
    search_fields = ('profile_item__name',)


@admin.register(models.ListEntry)
class ListEntryAdmin(admin.ModelAdmin):
    """
    Admin for the ``ListEntry`` model.
    """
    fields = ('list_content', 'text')
    list_display = ('string_repr', 'list_content')
    search_fields = ('text',)

    def string_repr(self, list_entry):
        """
        Get a string representation of a list entry.

        Args:
            list_entry:
                The list entry to get a string representation of.

        Returns:
            str:
                The provided list entry's string representation.
        """
        return str(list_entry)
    string_repr.admin_order_field = 'text'
    string_repr.short_description = _('text')


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin for the ``Profile`` model.
    """
    fields = ('name', 'user', 'quote', 'welcome_message')
    list_display = ('name', 'user')
    search_fields = ('name', 'user__first_name', 'user__last_name')


@admin.register(models.ProfileGroup)
class ProfileGroupAdmin(admin.ModelAdmin):
    """
    Admin for the ``ProfileGroup`` model.
    """
    fields = ('name', 'profile', 'is_default')
    list_display = ('name', 'profile', 'is_default')
    list_filter = ('is_default',)
    search_fields = ('name', 'profile__name')


@admin.register(models.ProfileItem)
class ProfileItemAdmin(admin.ModelAdmin):
    """
    Admin for the ``ProfileItem`` model.
    """
    fields = ('name', 'row', 'gallery_item', 'text')
    list_display = ('name', 'get_profile', 'get_group', 'row')
    search_fields = ('name',)

    def get_group(self, item):
        """
        Get the profile group the profile item belongs to.

        Args:
            item:
                The profile item to get the parent group of.

        Returns:
            The parent profile group of the given profile item.
        """
        return item.row.group
    get_group.admin_order_field = 'row__group'
    get_group.short_description = _('group')

    def get_profile(self, item):
        """
        Get the profile the profile item belongs to.

        Args:
            item:
                The profile item to get the parent profile of.

        Returns:
            The parent profile of the given profile item.
        """
        return item.row.group.profile
    get_profile.admin_order_field = 'row__group__profile'
    get_profile.short_description = _('profile')


@admin.register(models.ProfileRow)
class ProfileRowAdmin(admin.ModelAdmin):
    """
    Admin for the ``ProfileRow`` model.
    """
    fields = ('name', 'group', 'row_type')
    list_display = ('name', 'group', 'row_type')
    list_filter = ('row_type',)
    search_fields = ('group__name', 'name')
