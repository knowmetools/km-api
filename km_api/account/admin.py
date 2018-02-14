"""Admin configuration for the ``account`` module.
"""

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from account import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin for the ``User`` model.
    """
    fieldsets = (
        (_('Personal Info'), {
            'fields': ('first_name', 'last_name'),
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups',
                'user_permissions'
            ),
        }),
    )
    filter_horizontal = ('groups', 'user_permissions')
    list_display = ('first_name', 'last_name', 'is_staff', 'created_at')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'created_at')
    readonly_fields = ('created_at',)
    search_fields = ('first_name', 'last_name')
