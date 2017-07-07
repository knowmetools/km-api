from rest_framework.reverse import reverse

from know_me import models


def test_create(file, profile_factory):
    """
    Test creating a gallery item.
    """
    models.GalleryItem.objects.create(
        name='Gallery Item',
        profile=profile_factory(),
        resource=file)


def test_get_absolute_url(gallery_item_factory):
    """
    This method should return the URL of the galler item's detail view.
    """
    item = gallery_item_factory()
    expected = reverse('know-me:gallery-item-detail', kwargs={'pk': item.pk})

    assert item.get_absolute_url() == expected


def test_has_object_read_permission_other(
        api_rf,
        gallery_item_factory,
        user_factory):
    """
    Other users should not be able to read gallery items.
    """
    item = gallery_item_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not item.has_object_read_permission(request)


def test_has_object_read_permission_owner(api_rf, gallery_item_factory):
    """
    Users should have permission to read gallery items in their own
    profile.
    """
    item = gallery_item_factory()
    profile = item.profile

    api_rf.user = profile.user
    request = api_rf.get('/')

    assert item.has_object_read_permission(request)


def test_has_object_write_permission_other(
        api_rf,
        gallery_item_factory,
        user_factory):
    """
    Other users should not be able to write to gallery items they don't
    have access to.
    """
    item = gallery_item_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not item.has_object_write_permission(request)


def test_has_object_write_permission_owner(api_rf, gallery_item_factory):
    """
    Users should have write permissions on gallery items in their own
    profile.
    """
    item = gallery_item_factory()
    profile = item.profile

    api_rf.user = profile.user
    request = api_rf.get('/')

    assert item.has_object_write_permission(request)


def test_string_conversion(gallery_item_factory):
    """
    Converting a gallery item to a string should return the gallery
    item's name.
    """
    item = gallery_item_factory()

    assert str(item) == item.name
