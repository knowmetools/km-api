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
    expected = reverse(
        'know-me:gallery-item-detail',
        kwargs={
            'gallery_item_pk': item.pk,
            'profile_pk': item.profile.pk,
        })

    assert item.get_absolute_url() == expected


def test_string_conversion(gallery_item_factory):
    """
    Converting a gallery item to a string should return the gallery
    item's name.
    """
    item = gallery_item_factory()

    assert str(item) == item.name
