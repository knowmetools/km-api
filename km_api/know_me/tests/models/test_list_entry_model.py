from rest_framework.reverse import reverse

from know_me import models


def test_create_list_entry(list_content_factory):
    """
    Test creating a list entry.
    """
    models.ListEntry.objects.create(
            list_content=list_content_factory(),
            text='Test list entry.')


def test_get_absolute_url(list_entry_factory):
    """
    This method should return the URL for the list entry's detail view.
    """
    entry = list_entry_factory()
    expected = reverse('know-me:list-entry-detail', kwargs={'pk': entry.pk})

    assert entry.get_absolute_url() == expected


def test_string_conversion(list_entry_factory):
    """
    Converting a list entry to a string should return the entry's text.
    """
    entry = list_entry_factory()

    assert str(entry) == entry.text
