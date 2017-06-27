"""Admin objects for ``km_auth``.
"""


from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from km_auth import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin for the ``User`` model.
    """
    fieldsets = (
        (_('Personal Info'), {
            'fields': ('email', 'first_name', 'last_name'),
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups',
                'user_permissions'
            ),
        }),
    )
    filter_horizontal = ('groups', 'user_permissions')
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
