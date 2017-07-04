from rest_framework.reverse import reverse

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


def test_get_absolute_url(profile_item_factory):
    """
    This method should return the absolute URL of the profile item's
    detail view.
    """
    item = profile_item_factory()
    expected = reverse(
        'know-me:profile-item-detail',
        kwargs={
            'group_pk': item.row.group.pk,
            'item_pk': item.pk,
            'profile_pk': item.row.group.profile.pk,
            'row_pk': item.row.pk,
        })

    assert item.get_absolute_url() == expected


def test_string_conversion(profile_item_factory):
    """
    Converting a profile item to a string should return the profile
    item's name.
    """
    item = profile_item_factory()

    assert str(item) == item.name
