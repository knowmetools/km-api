"""Command for creating an admin user.
"""

import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from rest_email_auth.models import EmailAddress


class Command(BaseCommand):
    """
    Command to create an admin user.
    """
    help = ('Creates an admin user with the credentials given in the '
            'ADMIN_EMAIL and ADMIN_PASSWORD environment variables.')

    def handle(self, *args, **options):
        """
        Handle running the command.

        Args:
            args:
                Positional arguments given to the command.
            options:
                Keyword arguments given to the command.
        """
        email = os.environ['ADMIN_EMAIL']
        password = os.environ['ADMIN_PASSWORD']

        if EmailAddress.objects.filter(email=email).exists():
            email_instance = EmailAddress.objects.get(email=email)
            email_instance.is_verified = True
            email_instance.save()

            admin = email_instance.user
            admin.set_password(password)
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()

            self.stdout.write(self.style.NOTICE('Updated existing user.'))
        else:
            admin = get_user_model().objects.create_superuser(
                first_name='Admin',
                last_name='User',
                password=password)

            EmailAddress.objects.create(
                email=email,
                is_primary=True,
                is_verified=True,
                user=admin)

            self.stdout.write(self.style.NOTICE('Created new admin user.'))

        self.stdout.write(self.style.SUCCESS(
            'Successfully created admin user with a verified email address.'))
