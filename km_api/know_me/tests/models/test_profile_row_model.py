from rest_framework.reverse import reverse

from know_me import models


def test_create(profile_group_factory):
    """
    Test creating a profile row.
    """
    models.ProfileRow.objects.create(
        group=profile_group_factory(),
        name='Test Profile Row',
        row_type=models.ProfileRow.TEXT)


def test_get_absolute_url(profile_row_factory):
    """
    This method should return the URL of the row's detail view.
    """
    row = profile_row_factory()
    expected = reverse('know-me:profile-row-detail', kwargs={'pk': row.pk})

    assert row.get_absolute_url() == expected


def test_get_item_list_url(profile_row_factory):
    """
    This method should return the URL of the row's item list view.
    """
    row = profile_row_factory()
    expected = reverse('know-me:profile-item-list', kwargs={'pk': row.pk})

    assert row.get_item_list_url() == expected


def test_has_object_read_permission_other(
        api_rf,
        profile_row_factory,
        user_factory):
    """
    Users should not have read permissions on profile rows that belong
    to a profile they don't have access to.
    """
    row = profile_row_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not row.has_object_read_permission(request)


def test_has_object_read_permission_owner(api_rf, profile_row_factory):
    """
    Users should have read permissions on profile rows that belong to
    their own profile.
    """
    row = profile_row_factory()
    group = row.group
    profile = group.profile

    api_rf.user = profile.user
    request = api_rf.get('/')

    assert row.has_object_read_permission(request)


def test_has_object_write_permission_other(
        api_rf,
        profile_row_factory,
        user_factory):
    """
    Users should not have write permissions on profile rows that belong
    to a profile they don't have access to.
    """
    row = profile_row_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not row.has_object_write_permission(request)


def test_has_object_write_permission_owner(api_rf, profile_row_factory):
    """
    Users should have write permissions on profile rows that belong to
    their own profile.
    """
    row = profile_row_factory()
    group = row.group
    profile = group.profile

    api_rf.user = profile.user
    request = api_rf.get('/')

    assert row.has_object_write_permission(request)


def test_string_conversion(profile_row_factory):
    """
    Converting a profile row to a string should return the row's name.
    """
    row = profile_row_factory()

    assert str(row) == row.name
