"""Admin configuration for ``know_me`` module.
"""

from django.contrib import admin

from know_me import models


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
