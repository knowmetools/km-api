from unittest import mock

from know_me import models


def test_get_media_resource_upload_path():
    """
    Media Resources should be stored with their original filename in a
    folder titled ``profile/<id>/gallery``.
    """
    resource = mock.Mock(name='Mock Media Resource')
    resource.profile.id = 1

    filename = 'foo.jpg'

    expected = 'profile/{id}/gallery/{file}'.format(
        file=filename,
        id=resource.profile.id)

    result = models.get_media_resource_upload_path(resource, filename)
    assert result == expected


def test_km_user_image_upload_path():
    """
    """
    km_user = mock.Mock(name='Mock KM User')
    km_user.id = 1

    imagename = 'bar.jpg'

    expected = 'know-me/users/{id}/images/{file}'.format(
            file=imagename,
            id=km_user.id)

    assert models.get_km_user_image_upload_path(km_user, imagename) == expected
