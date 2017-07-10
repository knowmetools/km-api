"""Admin objects for the ``mailing_list`` module.
"""

from django.contrib import admin

from mailing_list import models


@admin.register(models.MailchimpUser)
class MailchimpUserAdmin(admin.ModelAdmin):
    """
    Admin for the ``MailchimpUser`` model.
    """
    fields = ('user', 'subscriber_hash')
    list_display = ('user',)
    search_fields = ('user__first_name', 'user__last_name')
