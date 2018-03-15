from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from watson import search

from know_me.journal import search_adapters


class JournalAppConfig(AppConfig):
    label = 'journal'
    name = 'know_me.journal'
    verbose_name = _('Know Me - Journal')

    def ready(self):
        """
        Register the journal entry model with django-watson.
        """
        Entry = self.get_model('Entry')

        search.register(
            Entry,
            search_adapters.EntrySearchAdapter,
            store=('text',))
