"""Signals for the ``mailing_list`` module.

These signals handle keeping a remote mailing list and the local user
accounts in sync.
"""

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from mailing_list import mailchimp_utils


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def mailchimp_sync(instance, **kwargs):
    """
    Sync a user's data to MailChimp if the integration is enabled.

    Args:
        instance:
            The user instance that was saved.
    """
    if getattr(settings, 'MAILCHIMP_ENABLED', False):
        mailchimp_utils.sync_mailchimp_data(
            settings.MAILCHIMP_LIST_ID,
            instance)
