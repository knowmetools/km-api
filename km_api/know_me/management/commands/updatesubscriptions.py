import datetime
import hashlib

from django.core import management
from django.db.models import Q
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
            is_active = False

            try:
                updated = subscriptions.validate_apple_receipt(
                    apple_sub.receipt_data
                )

                latest_hash = hashlib.sha256(
                    updated.latest_receipt_data.encode()
                ).hexdigest()

                unique_query = Q(latest_receipt_data_hash=latest_hash)
                unique_query |= Q(receipt_data_hash=latest_hash)

                if (
                    models.SubscriptionAppleData.objects.exclude(
                        pk=apple_sub.pk
                    )
                    .filter(unique_query)
                    .exists()
                ):
                    self.stdout.write(
                        self.style.NOTICE(
                            f"Apple receipt with ID {apple_sub.pk} has an "
                            f"updated hash that conflicts with another "
                            f"receipt: {latest_hash}"
                        )
                    )

                    is_active = False
                else:
                    apple_sub.expiration_time = updated.expires_date
                    apple_sub.latest_receipt_data = updated.latest_receipt_data
                    apple_sub.clean()
                    apple_sub.save()

                    if apple_sub.expiration_time > timezone.now():
                        is_active = True
            except subscriptions.ReceiptException:
                self.stdout.write(
                    self.style.NOTICE(
                        f"Apple receipt with ID {apple_sub.pk} failed "
                        f"verification."
                    )
                )

                # If there is an error verifying the receipt, the
                # subscription should be deactivated.
                is_active = False

            models.Subscription.objects.filter(apple_data=apple_sub).update(
                is_active=is_active
            )

        self.stdout.write(
            self.style.SUCCESS("Finished updating Apple subscriptions.")
        )
