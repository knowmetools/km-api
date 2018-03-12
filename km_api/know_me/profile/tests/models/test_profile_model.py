from unittest import mock

from rest_framework.reverse import reverse

from know_me.profile import models


def test_create(km_user_factory):
    """
    Test creating a profile.
    """
    models.Profile.objects.create(
        is_private=True,
        km_user=km_user_factory(),
        name='My Profile')


def test_get_absolute_url(profile_factory):
    """
    The profile's absolute URL should be the URL of its detail view.
    """
    profile = profile_factory()
    expected = reverse(
        'know-me:profile:profile-detail',
        kwargs={'pk': profile.pk})

    assert profile.get_absolute_url() == expected


def test_get_topic_list_url(profile_factory):
    """
    This method should return the absolute URL of the instance's topic
    list view.
    """
    profile = profile_factory()
    expected = reverse(
        'know-me:profile:profile-topic-list',
        kwargs={'pk': profile.pk})

    assert profile.get_topic_list_url() == expected


@mock.patch('know_me.models.KMUser.has_object_read_permission')
def test_has_object_read_permission(
        mock_parent_permission,
        api_rf,
        profile_factory):
    """
    Profiles should delegate the read permission check to their parent
    Know Me user.
    """
    profile = profile_factory()
    request = api_rf.get('/')

    expected = mock_parent_permission.return_value

    assert profile.has_object_read_permission(request) == expected
    assert mock_parent_permission.call_count == 1
    assert mock_parent_permission.call_args[0] == (request,)


@mock.patch('know_me.models.KMUser.has_object_write_permission')
def test_has_object_read_permission_private(
        mock_parent_permission,
        api_rf,
        profile_factory):
    """
    Private profiles should delegate their read permission check to
    their parent Know Me user's write permission check.

    Using the 'write' permission is intentional. Access to private
    profiles requires admin permissions, which is what write access to
    the parent Know Me user requires.
    """
    profile = profile_factory(is_private=True)
    request = api_rf.get('/')

    expected = mock_parent_permission.return_value

    assert profile.has_object_read_permission(request) == expected
    assert mock_parent_permission.call_count == 1
    assert mock_parent_permission.call_args[0] == (request,)


@mock.patch('know_me.models.KMUser.has_object_write_permission')
def test_has_object_write_permission(
        mock_parent_permission,
        api_rf,
        profile_factory):
    """
    Profiles should delegate the write permission check to their parent
    Know Me user.
    """
    profile = profile_factory()
    request = api_rf.get('/')

    expected = mock_parent_permission.return_value

    assert profile.has_object_write_permission(request) == expected
    assert mock_parent_permission.call_count == 1
    assert mock_parent_permission.call_args[0] == (request,)


def test_string_conversion(profile_factory):
    """
    Converting a profile instance to a string should return the
    profile's name.
    """
    profile = profile_factory()

    assert str(profile) == profile.name
