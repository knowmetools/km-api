"""Signals for the ``mailing_list`` module.

These signals handle keeping a remote mailing list and the local user
accounts in sync.
"""

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_email_auth.models import EmailAddress

from mailing_list import mailchimp_utils


def mailchimp_sync(user):
    """
    Sync a user's data to MailChimp if the integration is enabled.

    Args:
        user:
            The user instance that was saved.
    """
    if settings.MAILCHIMP_ENABLED:
        mailchimp_utils.sync_mailchimp_data(
            settings.MAILCHIMP_LIST_ID,
            user)


@receiver(post_save, sender=EmailAddress)
def mailchimp_email_signal(instance, created, **kwargs):
    """
    Trigger a MailChimp update when an email address is saved.

    Args:
        instance:
            The email address instance that was saved.
        created:
            A boolean indicating if the email was created or updated.
    """
    if instance.is_verified or not created:
        mailchimp_sync(instance.user)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def mailchimp_user_signal(instance, created, **kwargs):
    """
    Trigger a MailChimp update when a user is updated.

    Args:
        instance:
            The user instance that was saved.
        created:
            A boolean indicating if the user was created or updated.
    """
    if not created:
        mailchimp_sync(instance)
