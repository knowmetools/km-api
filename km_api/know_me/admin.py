"""Admin configuration for ``know_me`` module.
"""

from django.contrib import admin

from know_me import models


# Standard admin objects


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
        'can_write',
        'has_private_profile_access')
    list_display = (
        'km_user',
        'user_with_access',
        'accepted',
        'can_write',
        'has_private_profile_access')
    list_filter = ('accepted', 'can_write', 'has_private_profile_access')
    search_fields = (
        'km_user__user__first_name',
        'km_user__user__last_name',
        'user_with_access__first_name',
        'user_with_access__last_name')
