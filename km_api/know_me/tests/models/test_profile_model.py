from rest_framework.reverse import reverse

from know_me import models


def test_create(user_factory):
    """
    Test creating a km_user.
    """
    models.KMUser.objects.create(
        quote='Life is like a box of chocolates.',
        user=user_factory())


def test_get_absolute_url(km_user_factory):
    """
    This method should return the URL of the km_user's detail view.
    """
    km_user = km_user_factory()
    expected = reverse('know-me:km-user-detail', kwargs={'pk': km_user.pk})

    assert km_user.get_absolute_url() == expected


def test_get_gallery_url(km_user_factory):
    """
    This method should return the URL of the km_user's gallery view.
    """
    km_user = km_user_factory()
    expected = reverse('know-me:gallery', kwargs={'pk': km_user.pk})

    assert km_user.get_gallery_url() == expected


def test_get_profile_list_url(km_user_factory):
    """
    This method should return the URL of the profile's profile list view.
    """
    km_user = km_user_factory()
    expected = reverse('know-me:profile-list', kwargs={'pk': km_user.pk})

    assert km_user.get_profile_list_url() == expected


def test_has_object_read_permission_other(
        api_rf,
        km_user_factory,
        user_factory):
    """
    Other users should not have read permissions on km_users they don't
    own.
    """
    km_user = km_user_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not km_user.has_object_read_permission(request)


def test_has_object_read_permission_owner(api_rf, km_user_factory):
    """
    Users should have read access on their own km_user.
    """
    km_user = km_user_factory()

    api_rf.user = km_user.user
    request = api_rf.get('/')

    assert km_user.has_object_read_permission(request)


def test_has_object_write_permission_other(
        api_rf,
        km_user_factory,
        user_factory):
    """
    Other users should not have write permissions on km_users they don't
    own.
    """
    km_user = km_user_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not km_user.has_object_write_permission(request)


def test_has_object_write_permission_owner(api_rf, km_user_factory):
    """
    Users should have write access on their own km_user.
    """
    km_user = km_user_factory()

    api_rf.user = km_user.user
    request = api_rf.get('/')

    assert km_user.has_object_write_permission(request)


def test_string_conversion(km_user_factory):
    """
    Converting a km_user to a string should return the km_user's name.
    """
    km_user = km_user_factory()

    assert str(km_user) == km_user.user.get_short_name()
