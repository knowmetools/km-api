"""Admin configuration for ``know_me`` module.
"""

from django.contrib import admin

from know_me import models


@admin.register(models.GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    """
    Admin for the ``GalleryItem`` model.
    """
    fields = ('name', 'profile', 'resource')
    list_display = ('name', 'profile')
    search_fields = ('name', 'profile__name')


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


@admin.register(models.ProfileRow)
class ProfileRowAdmin(admin.ModelAdmin):
    """
    Admin for the ``ProfileRow`` model.
    """
    fields = ('name', 'group', 'row_type')
    list_display = ('name', 'group', 'row_type')
    list_filter = ('row_type',)
    search_fields = ('group__name', 'name')
