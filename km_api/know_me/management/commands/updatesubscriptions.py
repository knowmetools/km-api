import datetime

from django.core import management
from django.utils import timezone

from know_me import models, subscriptions


class Command(management.BaseCommand):
    """
    Management command to update the status of all subscriptions.
    """

    EXPIRATION_WINDOW = datetime.timedelta(hours=1)
    """
    The amount of time prior to an existing subscription's expiration
    date that we should begin updating it.
    """

    help = (
        "Update the validity and expiration status of all Know Me premium "
        "subscriptions."
    )

    def handle(self, *args, **options):
        """
        Execute the command.

        Args:
            *args:
                Positional arguments provided to the command.
            **options:
                Keyword arguments provided to the command.
        """
        self.stdout.write(
            "Deactivating all subscriptions without a receipt..."
        )
        orphan_sub_count = models.Subscription.objects.filter(
            apple_data__isnull=True, is_active=True
        ).update(is_active=False)
        self.stdout.write(
            f"Deactivated {orphan_sub_count} orphan subscription(s)."
        )

        cutoff_time = timezone.now() + self.EXPIRATION_WINDOW
        self.stdout.write(
            f"Updating Apple subscriptions that expire before "
            f"{cutoff_time.isoformat()}..."
        )

        query = models.SubscriptionAppleData.objects.filter(
            expiration_time__lte=cutoff_time
        )
        self.stdout.write(
            f"Found {query.count()} Apple subscription(s) to update."
        )

        for apple_sub in query:
            try:
                updated = subscriptions.validate_apple_receipt(
                    apple_sub.receipt_data
                )
                apple_sub.expiration_time = updated.expires_date
            except subscriptions.ReceiptException:
                self.stdout.write(
                    self.style.NOTICE(
                        f"Apple receipt with ID {apple_sub.pk} failed "
                        f"verification."
                    )
                )

            apple_sub.save()

        self.stdout.write(
            self.style.SUCCESS("Finished updating Apple subscriptions.")
        )
