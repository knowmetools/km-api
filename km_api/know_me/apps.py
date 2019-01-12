"""App configurations for the ``know_me`` module.
"""

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class KnowMeConfig(AppConfig):
    """
    Default app config.
    """

    name = "know_me"
    verbose_name = _("Know Me")

    def ready(self):
        """
        Perform app initialization tasks.
        """
        import know_me.signals  # noqa
