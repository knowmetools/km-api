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


def test_get_profile_list_url(km_user_factory):
    """
    This method should return the URL of the profile's list view.
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


def test_name(km_user_factory):
    """
    The know me user's name property should return the associated user's
    short name.
    """
    km_user = km_user_factory()

    assert km_user.name == km_user.user.get_short_name()


def test_share_existing_user(email_factory, km_user_factory, user_factory):
    """
    If the provided email address belongs to an existing user, an
    accessor should be created for that user.
    """
    km_user = km_user_factory()

    user = user_factory()

    accessor = km_user.share(
        user.primary_email.email,
        can_write=True,
        has_private_profile_access=True)

    assert km_user.km_user_accessors.count() == 1

    assert accessor.can_write
    assert accessor.email == user.primary_email.email
    assert accessor.has_private_profile_access
    assert accessor.user_with_access == user


def test_share_existing_user_unverified_email(
        email_factory,
        km_user_factory,
        user_factory):
    """
    If the provided email address exists but isn't verified, the
    accessor should not be assigned a user yet.
    """
    km_user = km_user_factory()

    user = user_factory()
    email = email_factory(is_verified=False, user=user)

    accessor = km_user.share(email.email)

    assert km_user.km_user_accessors.count() == 1

    assert accessor.email == email.email
    assert accessor.user_with_access is None


def test_share_nonexistent_user(km_user_factory):
    """
    If there is no user with the provided email address, The created
    accessor should only be linked to an email address.
    """
    km_user = km_user_factory()
    email = 'test-share@example.com'

    accessor = km_user.share(email)

    assert km_user.km_user_accessors.count() == 1

    assert accessor.email == email
    assert accessor.user_with_access is None


def test_string_conversion(km_user_factory):
    """
    Converting a km_user to a string should return the km_user's name.
    """
    km_user = km_user_factory()

    assert str(km_user) == km_user.name
