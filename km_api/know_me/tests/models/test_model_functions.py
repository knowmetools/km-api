from unittest import mock

from know_me import models


def test_get_media_resource_upload_path():
    """
    Media Resources should be stored with their original filename in a
    folder titled ``know-me/users/{id}/media-resources``.
    """
    resource = mock.Mock(name='Mock Media Resource')
    resource.km_user.id = 1

    filename = 'foo.jpg'

    expected = 'know-me/users/{id}/media-resources/{file}'.format(
        file=filename,
        id=resource.km_user.id)

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
