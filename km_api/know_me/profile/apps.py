from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ProfileAppConfig(AppConfig):
    label = "profile"
    name = "know_me.profile"
    verbose_name = _("Know Me - Profile")
