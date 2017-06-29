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
    expected = reverse(
        'know-me:profile-row-detail',
        kwargs={
            'group_pk': row.group.pk,
            'profile_pk': row.group.profile.pk,
            'row_pk': row.pk,
        })

    assert row.get_absolute_url() == expected


def test_string_conversion(profile_row_factory):
    """
    Converting a profile row to a string should return the row's name.
    """
    row = profile_row_factory()

    assert str(row) == row.name
