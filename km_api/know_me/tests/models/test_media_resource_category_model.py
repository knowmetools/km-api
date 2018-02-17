from rest_framework.reverse import reverse

from know_me import models


def test_create(km_user_factory):
    """
    Test creating a media resource category.
    """
    models.MediaResourceCategory.objects.create(
        km_user=km_user_factory(),
        name='Test Category')


def test_get_absolute_url(media_resource_category_factory):
    """
    This method should return the URL of the media resource category's detail
    view.
    """
    category = media_resource_category_factory()
    expected = reverse(
            'know-me:media-resource-category-detail',
            kwargs={'pk': category.pk})

    assert category.get_absolute_url() == expected


def test_has_object_read_permission_other(
        api_rf,
        media_resource_category_factory,
        user_factory):
    """
    Other users should not be able to read the media resource categories.
    """
    category = media_resource_category_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not category.has_object_read_permission(request)


def test_has_object_read_permission_owner(
        api_rf,
        media_resource_category_factory,
        user_factory):
    """
    Users should have read permission on media resource categories in their
    own km_user.
    """
    category = media_resource_category_factory()
    km_user = category.km_user

    api_rf.user = km_user.user
    request = api_rf.get('/')

    assert category.has_object_read_permission(request)


def test_has_object_write_permission_other(
        api_rf,
        media_resource_category_factory,
        user_factory):
    """
    Other users should not be able to write to media resource categories.
    """
    category = media_resource_category_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not category.has_object_write_permission(request)


def test_has_object_write_permission_owner(
        api_rf,
        media_resource_category_factory,
        user_factory):
    """
    Users should have write permissions on media resource in their own km_user.
    """
    category = media_resource_category_factory()
    km_user = category.km_user

    api_rf.user = km_user.user
    request = api_rf.get('/')

    assert category.has_object_write_permission(request)


def test_string_conversion(media_resource_category_factory):
    """
    Converting a media resource category to a string should return the
    category's name.
    """
    category = media_resource_category_factory()

    assert str(category) == category.name
