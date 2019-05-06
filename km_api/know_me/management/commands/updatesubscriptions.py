import datetime

from django.core import management
from django.utils import timezone

from know_me import models, subscriptions


class Command(management.BaseCommand):
    """
    Management command to update the status of all subscriptions.
    """

    RENEWAL_WINDOW = datetime.timedelta(hours=1)
    """
    The amount of time prior to an existing subscription's expiration
    date that we should begin attempting to renew it.
    """

    help = (
        "Update the validity and expiration status of all Know Me premium "
        "subscriptions."
    )

    @staticmethod
    def deactivate_orphan_subscriptions():
        """
        Deactivate all active subscriptions that do not have a payment
        method associated with them.

        The criteria for an orphan subscription are:

        1. Active subscription.
        2. No associated apple receipt.
        3. Not a legacy subscription.

        Returns:
            The number of deactivated subscriptions.
        """
        return models.Subscription.objects.filter(
            apple_receipt__isnull=True,
            is_legacy_subscription=False,
            is_active=True,
        ).update(is_active=False)

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
        orphan_subs = self.deactivate_orphan_subscriptions()
        self.stdout.write(f"Deactivated {orphan_subs} orphan subscription(s).")

        now = timezone.now()
        cutoff_time = now + self.RENEWAL_WINDOW
        self.stdout.write(
            f"Updating Apple subscriptions that expire before "
            f"{cutoff_time.isoformat()}..."
        )

        self.update_apple_subscriptions(now, self.RENEWAL_WINDOW)

        self.stdout.write(
            self.style.SUCCESS("Finished updating Apple subscriptions.")
        )

    def update_apple_subscriptions(
        self, now: datetime.datetime, renewal_window: datetime.timedelta
    ):
        """
        Attempt to renew Apple subscriptions that expire within the
        given cutoff time.

        Args:
            now:
                The time to compare receipt expiration times to to
                determine if they are expired.
            renewal_window:
                The amount of time before a receipt's expiration time
                that renewal should be attempted. In other words, all
                Apple receipts expiring before the current time plus
                this window will attempt to renew themselves.

        Returns:
            A dictionary containing counts for the different renewal
            outcomes.
        """
        receipts = models.AppleReceipt.objects.filter(
            expiration_time__lte=now + renewal_window
        )

        for receipt in receipts:
            is_active = True

            try:
                receipt.update_info()
                receipt.save()

                if receipt.expiration_time < now:
                    is_active = False
            except subscriptions.ReceiptException as e:
                self.stderr.write(
                    self.style.NOTICE(
                        f"Apple receipt {receipt.pk} failed validation: "
                        f"{e.msg}"
                    )
                )

                is_active = False

            models.Subscription.objects.filter(apple_receipt=receipt).update(
                is_active=is_active
            )
