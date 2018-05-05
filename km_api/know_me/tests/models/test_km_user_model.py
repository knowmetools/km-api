from django.core.exceptions import ValidationError

from rest_framework.reverse import reverse

import pytest

from know_me import models


def test_create(user_factory):
    """
    Test creating a km_user.
    """
    km_user = models.KMUser.objects.create(
        quote='Life is like a box of chocolates.',
        user=user_factory())

    assert not km_user.is_legacy_user


def test_get_absolute_url(km_user_factory):
    """
    This method should return the URL of the km_user's detail view.
    """
    km_user = km_user_factory()
    expected = reverse('know-me:km-user-detail', kwargs={'pk': km_user.pk})

    assert km_user.get_absolute_url() == expected


def test_get_media_resource_category_list_url(km_user_factory):
    """
    This method should return the URL of the Know Me user's media
    resource category list view.
    """
    km_user = km_user_factory()
    expected = reverse(
        'know-me:profile:media-resource-category-list',
        kwargs={'pk': km_user.pk})

    assert km_user.get_media_resource_category_list_url() == expected


def test_get_media_resource_category_list_url_request(api_rf, km_user_factory):
    """
    If given a request as context, the method should return the full URI
    if the Know Me user's media resource category list view.
    """
    km_user = km_user_factory()
    request = api_rf.get(km_user.get_media_resource_category_list_url())
    expected = request.build_absolute_uri()

    assert km_user.get_media_resource_category_list_url(request) == expected


def test_get_media_resource_list_url(km_user_factory):
    """
    This method should return the absolute URL of the Know Me user's
    media resource list view.
    """
    km_user = km_user_factory()
    expected = reverse(
        'know-me:profile:media-resource-list',
        kwargs={'pk': km_user.pk})

    assert km_user.get_media_resource_list_url() == expected


def test_get_profile_list_url(km_user_factory):
    """
    This method should return the URL of the Know Me user's profile list
    view.
    """
    km_user = km_user_factory()
    expected = reverse(
        'know-me:profile:profile-list',
        kwargs={'pk': km_user.pk})

    assert km_user.get_profile_list_url() == expected


def test_get_profile_list_url_request(api_rf, km_user_factory):
    """
    If given a request as context, the method should return the full URI
    of the Know Me user's profile list view.
    """
    km_user = km_user_factory()
    request = api_rf.get(km_user.get_profile_list_url())
    expected = request.build_absolute_uri()

    assert km_user.get_profile_list_url(request) == expected


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


def test_has_object_read_permission_shared(
        api_rf,
        km_user_accessor_factory,
        km_user_factory):
    """
    The requesting user should be granted read access if there is an
    accessor granting them access.
    """
    km_user = km_user_factory()
    accessor = km_user_accessor_factory(is_accepted=True, km_user=km_user)

    api_rf.user = accessor.user_with_access
    request = api_rf.get('/')

    assert km_user.has_object_read_permission(request)


def test_has_object_read_permission_shared_not_accepted(
        api_rf,
        km_user_accessor_factory,
        km_user_factory):
    """
    If the accessor granting access has not been accepted yet, access
    should not be granted.
    """
    km_user = km_user_factory()
    accessor = km_user_accessor_factory(is_accepted=False, km_user=km_user)

    api_rf.user = accessor.user_with_access
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


def test_has_object_write_permission_shared(
        api_rf,
        km_user_accessor_factory,
        km_user_factory):
    """
    Users should be able to be granted write access through an accessor.
    """
    km_user = km_user_factory()
    accessor = km_user_accessor_factory(
        is_accepted=True,
        is_admin=True,
        km_user=km_user)

    api_rf.user = accessor.user_with_access
    request = api_rf.get('/')

    assert km_user.has_object_write_permission(request)


def test_has_object_write_permission_shared_no_write(
        api_rf,
        km_user_accessor_factory,
        km_user_factory):
    """
    Write access should not be granted from accessors that only grant
    read access.
    """
    km_user = km_user_factory()
    accessor = km_user_accessor_factory(
        is_accepted=True,
        is_admin=False,
        km_user=km_user)

    api_rf.user = accessor.user_with_access
    request = api_rf.get('/')

    assert not km_user.has_object_write_permission(request)


def test_has_object_write_permission_shared_not_accepted(
        api_rf,
        km_user_accessor_factory,
        km_user_factory):
    """
    If the accessor has not been accepted, it should not grant write
    access.
    """
    km_user = km_user_factory()
    accessor = km_user_accessor_factory(
        is_accepted=False,
        is_admin=True,
        km_user=km_user)

    api_rf.user = accessor.user_with_access
    request = api_rf.get('/')

    assert not km_user.has_object_write_permission(request)


def test_name(km_user_factory):
    """
    The know me user's name property should return the associated user's
    short name.
    """
    km_user = km_user_factory()

    assert km_user.name == km_user.user.get_short_name()


def test_share_duplicate_email(
        email_factory,
        km_user_accessor_factory,
        km_user_factory):
    """
    If there is already an accessor linking the provided email and Know
    Me user, a validation error should be raised.
    """
    km_user = km_user_factory()
    email = email_factory()
    km_user_accessor_factory(email=email.email, km_user=km_user)

    with pytest.raises(ValidationError):
        km_user.share(email.email)


def test_share_existing_user(email_factory, km_user_factory, user_factory):
    """
    If the provided email address belongs to an existing user, an
    accessor should be created for that user.
    """
    km_user = km_user_factory()

    user = user_factory()

    accessor = km_user.share(
        user.primary_email.email,
        is_admin=True)

    assert km_user.km_user_accessors.count() == 1

    assert accessor.email == user.primary_email.email
    assert accessor.is_admin


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


def test_share_multiple_emails(
        email_factory,
        km_user_accessor_factory,
        km_user_factory,
        user_factory):
    """
    If a user has already been granted access through another email that
    they own, they should not be able to be granted access through
    another email address that they own.
    """
    user = user_factory()
    e1 = email_factory(is_verified=True, user=user)
    e2 = email_factory(is_verified=True, user=user)

    km_user = km_user_factory()
    km_user_accessor_factory(email=e1, km_user=km_user, user_with_access=user)

    with pytest.raises(ValidationError):
        km_user.share(e2.email)


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
