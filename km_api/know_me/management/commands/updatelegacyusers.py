from django.core import management
from django.db.models import Q

from know_me import models


class Command(management.BaseCommand):
    """
    Link legacy users to Know Me users by email address.
    """

    help = (
        "Mark Know Me users who have a verified email address corresponding "
        "to a legacy user's email address as legacy users."
    )

    def handle(self, *args, **options):
        """
        Entry point into the command.
        """
        legacy_count = models.LegacyUser.objects.count()
        self.stdout.write(f"Processing {legacy_count} legacy user(s)")

        verified_user_ids = []

        for user in models.LegacyUser.objects.all():
            query = Q(user__email_address__email=user.email)
            query &= Q(user__email_address__is_verified=True)

            if models.KMUser.objects.filter(query).update(is_legacy_user=True):
                self.stdout.write(
                    f"Associated legacy user with email address {user.email}"
                )

                verified_user_ids.append(user.pk)

        models.LegacyUser.objects.filter(pk__in=verified_user_ids).delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Marked {len(verified_user_ids)} new legacy user(s)."
            )
        )
