"""Admin configuration for the ``account`` module.
"""

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from account import models


@admin.register(models.EmailConfirmation)
class EmailConfirmationAdmin(admin.ModelAdmin):
    """
    Admin for ``EmailConfirmation`` instances.
    """
    fields = ('user', 'created_at', 'key')
    list_display = ('user', 'created_at')
    readonly_fields = ('user', 'created_at', 'key',)
    search_fields = ('user__email',)

    def has_add_permission(self, request):
        """
        Disable adding new email confirmations.

        Args:
            request:
                The request being made.

        Returns:
            bool:
                ``False``
        """
        return False


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin for the ``User`` model.
    """
    fieldsets = (
        (_('Personal Info'), {
            'fields': ('email', 'email_verified', 'first_name', 'last_name'),
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups',
                'user_permissions'
            ),
        }),
    )
    filter_horizontal = ('groups', 'user_permissions')
    list_display = (
        'email', 'email_verified', 'first_name', 'last_name', 'is_staff'
    )
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
