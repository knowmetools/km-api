"""App configurations for the ``mailing_list`` module.
"""

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MailingListAppConfig(AppConfig):
    """
    Default app configuration.
    """
    name = 'mailing_list'
    verbose_name = _('mailing list')

    def ready(self):
        """
        Initialize app.

        This method allows us to defer initialiazation tasks such as
        loading signals until after the app's models are ready.
        """
        from mailing_list.signals import (      # noqa
            mailchimp_email_signal,
            mailchimp_user_signal,
        )
