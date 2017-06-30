from know_me import models


def test_create(gallery_item_factory, profile_row_factory):
    """
    Test creating a profile item.
    """
    models.ProfileItem.objects.create(
        gallery_item=gallery_item_factory(),
        name='Profile Item',
        row=profile_row_factory(),
        text='Some sample item text.')


def test_string_conversion(profile_item_factory):
    """
    Converting a profile item to a string should return the profile
    item's name.
    """
    item = profile_item_factory()

    assert str(item) == item.name
