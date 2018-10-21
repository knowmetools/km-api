from django.contrib import admin

from know_me import models


class AppleSubscriptionInline(admin.StackedInline):
    """
    Inline admin editor for Apple subscription data.
    """
    fields = ('receipt_data', 'time_created', 'time_updated')
    model = models.SubscriptionAppleData
    readonly_fields = ('time_created', 'time_updated')


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Admin for Know Me subscriptions.
    """
    autocomplete_fields = ('user',)
    date_hierarchy = 'time_created'
    fields = ('user', 'is_active', 'time_created', 'time_updated')
    inlines = (AppleSubscriptionInline,)
    readonly_fields = ('time_created', 'time_updated')
    list_display = ('user', 'is_active', 'time_created', 'time_updated')
    list_filter = ('is_active',)
    search_fields = ('user__first_name', 'user__last_name')
