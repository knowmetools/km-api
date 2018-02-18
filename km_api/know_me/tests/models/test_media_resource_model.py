from rest_framework.reverse import reverse

from know_me import models


def test_create(file, km_user_factory, media_resource_category_factory):
    """
    Test creating a media resource.
    """
    models.MediaResource.objects.create(
        category=media_resource_category_factory(),
        name='Media Resource',
        km_user=km_user_factory(),
        file=file)


def test_get_absolute_url(media_resource_factory):
    """
    This method should return the URL of the media resources detail
    view.
    """
    resource = media_resource_factory()
    expected = reverse(
            'know-me:media-resource-detail',
            kwargs={'pk': resource.pk})

    assert resource.get_absolute_url() == expected


def test_has_object_read_permission_other(
        api_rf,
        media_resource_factory,
        user_factory):
    """
    Other users should not be able to read media resources.
    """
    resource = media_resource_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not resource.has_object_read_permission(request)


def test_has_object_read_permission_owner(api_rf, media_resource_factory):
    """
    Users should have permission to read media resources in their own
    km_user.
    """
    resource = media_resource_factory()
    km_user = resource.km_user

    api_rf.user = km_user.user
    request = api_rf.get('/')

    assert resource.has_object_read_permission(request)


def test_has_object_write_permission_other(
        api_rf,
        media_resource_factory,
        user_factory):
    """
    Other users should not be able to write to media resources they
    don't have access to.
    """
    resource = media_resource_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not resource.has_object_write_permission(request)


def test_has_object_write_permission_owner(api_rf, media_resource_factory):
    """
    Users should have write permissions on media resource in their
    own km_user.
    """
    resource = media_resource_factory()
    km_user = resource.km_user

    api_rf.user = km_user.user
    request = api_rf.get('/')

    assert resource.has_object_write_permission(request)


def test_string_conversion(media_resource_factory):
    """
    Converting a media resource to a string should return the media
    resource's name.
    """
    resource = media_resource_factory()

    assert str(resource) == resource.name
