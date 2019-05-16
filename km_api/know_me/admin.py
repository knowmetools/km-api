from django.contrib import admin

from know_me import models


class AppleReceiptInline(admin.StackedInline):
    """
    Inline admin editor for Apple receipts.
    """

    fields = (
        "receipt_data",
        "expiration_time",
        "transaction_id",
        "time_created",
        "time_updated",
    )
    model = models.AppleReceipt
    readonly_fields = (
        "expiration_time",
        "time_created",
        "time_updated",
        "transaction_id",
    )


@admin.register(models.KMUser)
class KMUserAdmin(admin.ModelAdmin):
    """
    Admin for Know Me users.
    """

    autocomplete_fields = ("user",)
    date_hierarchy = "created_at"
    fields = (
        "user",
        "image",
        "is_legacy_user",
        "quote",
        "created_at",
        "updated_at",
    )
    list_display = ("user", "is_legacy_user", "created_at", "updated_at")
    list_filter = ("is_legacy_user",)
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("user__first_name", "user__last_name")


@admin.register(models.LegacyUser)
class LegacyUserAdmin(admin.ModelAdmin):
    """
    Admin for legacy Know Me users.
    """

    date_hierarchy = "created_at"
    fields = ("email", "created_at", "updated_at")
    list_display = ("email", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("email",)


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Admin for Know Me subscriptions.
    """

    autocomplete_fields = ("user",)
    date_hierarchy = "time_created"
    fields = ("user", "is_active", "time_created", "time_updated")
    inlines = (AppleReceiptInline,)
    readonly_fields = ("time_created", "time_updated")
    list_display = ("user", "is_active", "time_created", "time_updated")
    list_filter = ("is_active",)
    search_fields = ("user__first_name", "user__last_name")
