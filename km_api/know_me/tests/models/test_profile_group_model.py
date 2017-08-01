from rest_framework.reverse import reverse

from know_me import models


def test_create(km_user_factory):
    """
    Test creating a profile.
    """
    models.Profile.objects.create(
        is_default=True,
        name='Profile Group',
        km_user=km_user_factory())


def test_get_absolute_url(profile_factory):
    """
    This method should return the URL of the profile's detail
    view.
    """
    profile = profile_factory()
    expected = reverse('know-me:profile-detail', kwargs={'pk': profile.pk})

    assert profile.get_absolute_url() == expected


def test_get_topic_list_url(profile_factory):
    """
    This method should return the URL of the profile's topic list
    view.
    """
    profile = profile_factory()
    expected = reverse('know-me:profile-topic-list', kwargs={'pk': profile.pk})

    assert profile.get_topic_list_url() == expected


def test_has_object_read_permission_other(
        api_rf,
        profile_factory,
        user_factory):
    """
    Users should not have read permissions on profiles that are
    not part of a km_user they have access to.
    """
    profile = profile_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not profile.has_object_read_permission(request)


def test_has_object_read_permission_owner(api_rf, profile_factory):
    """
    Users should have read permissions on profiles that belong to
    their own km_user.
    """
    profile = profile_factory()
    km_user = profile.km_user

    api_rf.user = km_user.user
    request = api_rf.get('/')

    assert profile.has_object_read_permission(request)


def test_has_object_write_permission_other(
        api_rf,
        profile_factory,
        user_factory):
    """
    Users should not have write permissions on profiles that are
    not part of a km_user they have access to.
    """
    profile = profile_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not profile.has_object_write_permission(request)


def test_has_object_write_permission_owner(api_rf, profile_factory):
    """
    Users should have write permissions on profiles that belong to
    their own km_user.
    """
    profile = profile_factory()
    km_user = profile.km_user

    api_rf.user = km_user.user
    request = api_rf.get('/')

    assert profile.has_object_write_permission(request)


def test_string_conversion(profile_factory):
    """
    Converting a profile to a string should return the profile's
    name.
    """
    profile = profile_factory()

    assert str(profile) == profile.name
