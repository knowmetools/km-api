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
