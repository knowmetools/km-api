from know_me import models


def test_create(profile_group_factory):
    """
    Test creating a profile row.
    """
    models.ProfileRow.objects.create(
        group=profile_group_factory(),
        name='Test Profile Row',
        row_type=models.ProfileRow.TEXT)


def test_string_conversion(profile_row_factory):
    """
    Converting a profile row to a string should return the row's name.
    """
    row = profile_row_factory()

    assert str(row) == row.name
