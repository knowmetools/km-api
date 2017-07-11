"""Models for the ``account`` module.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from account import managers


class EmailConfirmation(models.Model):
    """
    Model that allows validation of an email address.

    The confirmation contains a link to a user, a key, and an expiration
    date. An email can be validated by checking that the confirmation
    has not expired and that the provided key matches the confirmation's
    key.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at'))
    key = models.CharField(
        max_length=settings.EMAIL_CONFIRMATION_KEY_LENGTH,
        unique=True,
        verbose_name=_('key'))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('user'))

    objects = managers.EmailConfirmationManager()

    class Meta:
        verbose_name = _('email confirmation')
        verbose_name_plural = _('email confirmations')

    def __str__(self):
        """
        Get a string representation of the instance.

        Returns:
            str:
                A string containing a message indicating which email
                address the confirmation is for.
        """
        return ugettext(
            'Confirmation for %(email)s' % {
                'email': self.user.email,
            })
