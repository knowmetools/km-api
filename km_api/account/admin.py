"""Admin configuration for the ``account`` module.
"""

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from account import models


@admin.register(models.EmailAddress)
class EmailAddressAdmin(admin.ModelAdmin):
    """
    Admin for ``EmailAddress`` instances.
    """
    fields = ('email', 'user', 'primary', 'verified')
    list_display = ('email', 'user', 'verified', 'primary')
    search_fields = ('email', 'user__first_name', 'user__last_name')


@admin.register(models.EmailConfirmation)
class EmailConfirmationAdmin(admin.ModelAdmin):
    """
    Admin for ``EmailConfirmation`` instances.
    """
    fields = ('email__email', 'created_at', 'key')
    list_display = ('email', 'created_at')
    readonly_fields = ('created_at', 'key',)
    search_fields = ('email__email',)

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
