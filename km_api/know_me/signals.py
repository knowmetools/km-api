import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_email_auth.models import EmailAddress

from know_me import models


logger = logging.getLogger(__name__)


@receiver(post_save, sender=EmailAddress)
def update_accessor(instance, **kwargs):
    """
    Update accessors that have an email address but no user.

    If the accessor has an email address only and that email is now
    verified, the accessor is updated to point to the user who owns the
    email address.

    Args:
        instance:
            The email address that was just saved.
    """
    logger.debug(
        'Updating KMUserAccessor instances for email %s',
        instance.email)

    try:
        accessor = models.KMUserAccessor.objects.get(
            email=instance.email,
            user_with_access=None)
    except models.KMUserAccessor.DoesNotExist:
        return

    if instance.is_verified:
        dupe_query = accessor.km_user.km_user_accessors.filter(
            user_with_access=instance.user)

        if dupe_query.exists():
            duplicate = dupe_query.get()
            logger.warning(
                "Deleting accessor linking %s and %s because the user has "
                "been granted access through the email address %s",
                instance.email,
                '{} (ID: {})'.format(accessor.km_user, accessor.km_user.id),
                duplicate.email)
            accessor.delete()

            return

        accessor.user_with_access = instance.user
        accessor.save()

        logger.info('Updated KMUserAccessor for email %s', instance.email)
