"""Command for creating an admin user.
"""

import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from account import models


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

        admin = get_user_model().objects.create_superuser(
            email=email,
            first_name='Admin',
            last_name='User',
            password=password)

        models.EmailAddress.objects.create(
            email=email,
            primary=True,
            verified=True,
            user=admin)

        self.stdout.write(self.style.SUCCESS(
            'Successfully created admin user with a verified email address.'))
