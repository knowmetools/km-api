from unittest import mock

from know_me import models


def test_get_gallery_item_upload_path():
    """
    Gallery items should be stored with their original filename in a
    folder titled ``profile/<id>/gallery``.
    """
    item = mock.Mock(name='Mock Gallery Item')
    item.profile.id = 1

    filename = 'foo.jpg'

    expected = 'profile/{id}/gallery/{file}'.format(
        file=filename,
        id=item.profile.id)

    assert models.get_gallery_item_upload_path(item, filename) == expected
