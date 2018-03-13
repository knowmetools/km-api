from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class JournalAppConfig(AppConfig):
    label = 'journal'
    name = 'know_me.journal'
    verbose_name = _('Know Me - Journal')
