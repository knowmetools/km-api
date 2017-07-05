from rest_framework.reverse import reverse

from know_me import models


def test_create(user_factory):
    """
    Test creating a profile.
    """
    models.Profile.objects.create(
        name='John',
        quote='Life is like a box of chocolates.',
        user=user_factory(),
        welcome_message="Hi, I'm John")


def test_get_absolute_url(profile_factory):
    """
    This method should return the URL of the profile's detail view.
    """
    profile = profile_factory()
    expected = reverse(
        'know-me:profile-detail',
        kwargs={'profile_pk': profile.pk})

    assert profile.get_absolute_url() == expected


def test_get_gallery_url(profile_factory):
    """
    This method should return the URL of the profile's gallery view.
    """
    profile = profile_factory()
    expected = reverse('know-me:gallery', kwargs={'profile_pk': profile.pk})

    assert profile.get_gallery_url() == expected


def test_get_group_list_url(profile_factory):
    """
    This method should return the URL of the profile's group list view.
    """
    profile = profile_factory()
    expected = reverse(
        'know-me:profile-group-list',
        kwargs={'profile_pk': profile.pk})

    assert profile.get_group_list_url() == expected


def test_has_object_read_permission_other(
        api_rf,
        profile_factory,
        user_factory):
    """
    Other users should not have read permissions on profiles they don't
    own.
    """
    profile = profile_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not profile.has_object_read_permission(request)


def test_has_object_read_permission_owner(api_rf, profile_factory):
    """
    Users should have read access on their own profile.
    """
    profile = profile_factory()

    api_rf.user = profile.user
    request = api_rf.get('/')

    assert profile.has_object_read_permission(request)


def test_has_object_write_permission_other(
        api_rf,
        profile_factory,
        user_factory):
    """
    Other users should not have write permissions on profiles they don't
    own.
    """
    profile = profile_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not profile.has_object_write_permission(request)


def test_has_object_write_permission_owner(api_rf, profile_factory):
    """
    Users should have write access on their own profile.
    """
    profile = profile_factory()

    api_rf.user = profile.user
    request = api_rf.get('/')

    assert profile.has_object_write_permission(request)


def test_string_conversion(profile_factory):
    """
    Converting a profile to a string should return the profile's name.
    """
    profile = profile_factory()

    assert str(profile) == profile.name
