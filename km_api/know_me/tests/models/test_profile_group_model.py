from rest_framework.reverse import reverse

from know_me import models


def test_create(profile_factory):
    """
    Test creating a profile group.
    """
    models.ProfileGroup.objects.create(
        is_default=True,
        name='Profile Group',
        profile=profile_factory())


def test_get_absolute_url(profile_group_factory):
    """
    This method should return the URL of the profile group's detail
    view.
    """
    group = profile_group_factory()
    expected = reverse(
        'know-me:profile-group-detail',
        kwargs={
            'group_pk': group.pk,
            'profile_pk': group.profile.pk,
        })

    assert group.get_absolute_url() == expected


def test_string_conversion(profile_group_factory):
    """
    Converting a profile group to a string should return the group's
    name.
    """
    group = profile_group_factory()

    assert str(group) == group.name
