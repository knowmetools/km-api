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
    expected = reverse('know-me:profile-group-detail', kwargs={'pk': group.pk})

    assert group.get_absolute_url() == expected


def test_get_topic_list_url(profile_group_factory):
    """
    This method should return the URL of the profile group's topic list
    view.
    """
    group = profile_group_factory()
    expected = reverse('know-me:profile-topic-list', kwargs={'pk': group.pk})

    assert group.get_topic_list_url() == expected


def test_has_object_read_permission_other(
        api_rf,
        profile_group_factory,
        user_factory):
    """
    Users should not have read permissions on profile groups that are
    not part of a profile they have access to.
    """
    group = profile_group_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not group.has_object_read_permission(request)


def test_has_object_read_permission_owner(api_rf, profile_group_factory):
    """
    Users should have read permissions on profile groups that belong to
    their own profile.
    """
    group = profile_group_factory()
    profile = group.profile

    api_rf.user = profile.user
    request = api_rf.get('/')

    assert group.has_object_read_permission(request)


def test_has_object_write_permission_other(
        api_rf,
        profile_group_factory,
        user_factory):
    """
    Users should not have write permissions on profile groups that are
    not part of a profile they have access to.
    """
    group = profile_group_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not group.has_object_write_permission(request)


def test_has_object_write_permission_owner(api_rf, profile_group_factory):
    """
    Users should have write permissions on profile groups that belong to
    their own profile.
    """
    group = profile_group_factory()
    profile = group.profile

    api_rf.user = profile.user
    request = api_rf.get('/')

    assert group.has_object_write_permission(request)


def test_string_conversion(profile_group_factory):
    """
    Converting a profile group to a string should return the group's
    name.
    """
    group = profile_group_factory()

    assert str(group) == group.name
