from know_me import models


def test_create(profile_factory):
    """
    Test creating a profile group.
    """
    models.ProfileGroup.objects.create(
        is_default=True,
        name='Profile Group',
        profile=profile_factory())


def test_string_conversion(profile_group_factory):
    """
    Converting a profile group to a string should return the group's
    name.
    """
    group = profile_group_factory()

    assert str(group) == group.name
