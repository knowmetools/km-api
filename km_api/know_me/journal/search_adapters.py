from watson import search


class EntrySearchAdapter(search.SearchAdapter):
    """
    Search adapter for the ``Entry`` model.
    """

    def get_content(self, obj):
        return obj.text
