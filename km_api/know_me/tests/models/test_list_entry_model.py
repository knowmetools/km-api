from know_me import models


def test_create_list_entry(list_content_factory):
    """
    Test creating a list entry.
    """
    models.ListEntry.objects.create(
        list_content=list_content_factory(),
        text='Test list entry')


def test_string_conversion(list_entry_factory):
    """
    Converting a list entry to a string should return a message
    containing the list entry's text.
    """
    entry = list_entry_factory()

    assert str(entry) == entry.text


def test_string_conversion_long_text(list_entry_factory):
    """
    Converting a list entry with a long text message to a string should
    return the entry's message truncated to be 50 characters long.
    """
    text = 'This is a really long piece of text that needs to be truncated.'
    entry = list_entry_factory(text=text)

    expected = '{}...'.format(text[:47])

    assert str(entry) == expected
