from know_me import models


def test_create(file, profile_factory):
    """
    Test creating a gallery item.
    """
    models.GalleryItem.objects.create(
        name='Gallery Item',
        profile=profile_factory(),
        resource=file)


def test_string_conversion(gallery_item_factory):
    """
    Converting a gallery item to a string should return the gallery
    item's name.
    """
    item = gallery_item_factory()

    assert str(item) == item.name
