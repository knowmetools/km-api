"""App configurations for ``km_auth``.
"""

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class KMAuthConfig(AppConfig):
    """
    Default app configuration.
    """
    name = 'km_auth'
    verbose_name = _('Know Me Authentication and Authorization')
