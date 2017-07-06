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
    expected = reverse('know-me:profile-item-detail', kwargs={'pk': item.pk})

    assert item.get_absolute_url() == expected


def test_has_object_read_permission_other(
        api_rf,
        profile_item_factory,
        user_factory):
    """
    Users should not have read permissions on profile items that belong
    to a profile they don't have access to.
    """
    item = profile_item_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not item.has_object_read_permission(request)


def test_has_object_read_permission_owner(api_rf, profile_item_factory):
    """
    Users should have read permissions on profile items belonging to
    their own profile.
    """
    item = profile_item_factory()
    row = item.row
    group = row.group
    profile = group.profile

    api_rf.user = profile.user
    request = api_rf.get('/')

    assert item.has_object_read_permission(request)


def test_has_object_write_permission_other(
        api_rf,
        profile_item_factory,
        user_factory):
    """
    Users should not have write permissions on profile items that belong
    to a profile they don't have access to.
    """
    item = profile_item_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not item.has_object_write_permission(request)


def test_has_object_write_permission_owner(api_rf, profile_item_factory):
    """
    Users should have write permissions on profile items belonging to
    their own profile.
    """
    item = profile_item_factory()
    row = item.row
    group = row.group
    profile = group.profile

    api_rf.user = profile.user
    request = api_rf.get('/')

    assert item.has_object_write_permission(request)


def test_string_conversion(profile_item_factory):
    """
    Converting a profile item to a string should return the profile
    item's name.
    """
    item = profile_item_factory()

    assert str(item) == item.name
