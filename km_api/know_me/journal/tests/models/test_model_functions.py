from unittest import mock

from know_me.journal import models


def test_get_entry_attachment_upload_path():
    """
    Test getting the path that a journal entry's attachment is uploaded
    to.
    """
    entry = mock.Mock(name="Mock Entry")
    entry.km_user.id = 1
    filename = "foo.jpg"

    result = models.get_entry_attachment_upload_path(entry, filename)
    expected = "know-me/users/{id}/journal/attachments/{file}".format(
        file=filename, id=entry.km_user.id
    )

    assert result == expected
