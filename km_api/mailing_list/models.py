"""Models for keeping track of mailing list information.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class MailchimpUser(models.Model):
    """
    A link between a user and MailChimp list member.

    Attributes:
        subscriber_hash (str):
            The hash MailChimp uses to identify a user. This also allows
            us to update the list information when a user changes their
            email address.
        user:
            The user linked to the MailChimp member.
    """
    subscriber_hash = models.CharField(
        max_length=32,
        verbose_name=_('subscriber hash'))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mailchimp_users',
        related_query_name='mailchimp_user',
        verbose_name=_('user'))

    class Meta:
        verbose_name = _('MailChimp user')
        verbose_name_plural = _('MailChimp users')
