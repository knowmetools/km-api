"""Admin configuration for the ``account`` module.
"""

from django.contrib import admin

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
