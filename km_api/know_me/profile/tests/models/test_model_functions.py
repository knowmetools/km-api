from unittest import mock

from know_me.profile import models


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


def test_get_profile_item_image_upload_path():
    """
    Profile item images should be stored with their original filename in
    a directory titled ``know-me/users/{id}/profile-images``.
    """
    profile_item = mock.Mock(name='Mock Profile Item')
    profile_item.topic.profile.km_user.id = 1
    filename = 'image.jpg'

    result = models.get_profile_item_image_upload_path(profile_item, filename)
    expected = 'know-me/users/{id}/profile-images/{file}'.format(
        file=filename,
        id=profile_item.topic.profile.km_user.id)\

    assert result == expected
