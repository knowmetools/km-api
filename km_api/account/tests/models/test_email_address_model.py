from rest_framework.reverse import reverse

from account import models


def test_create_email(user_factory):
    """
    Test creating an email.
    """
    email = models.EmailAddress.objects.create(
        email='test@example.com',
        user=user_factory(),
        verified_action=models.EmailAddress.REPLACE_PRIMARY)

    assert not email.verified


def test_create_duplicate_unverified(email_factory):
    """
    If an email address is unverified, it should still be possible to
    create another instance of that email address.
    """
    email = email_factory(verified=False)

    email_factory(email=email.email)


def test_get_absolute_url(email_factory):
    """
    The method should return the URL of the email address' detail view.
    """
    email = email_factory()
    expected = reverse('account:email-detail', kwargs={'pk': email.pk})

    assert email.get_absolute_url() == expected


def test_has_object_read_permission_other(api_rf, email_factory, user_factory):
    """
    User should not have read permissions on other users' email
    addresses.
    """
    email = email_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not email.has_object_read_permission(request)


def test_has_object_read_permission_owner(api_rf, email_factory):
    """
    Users should have read permissions on their own email addresses.
    """
    email = email_factory()

    api_rf.user = email.user
    request = api_rf.get('/')

    assert email.has_object_read_permission(request)


def test_has_object_write_permission_other(
        api_rf,
        email_factory,
        user_factory):
    """
    User should not have write permissions on other users' email
    addresses.
    """
    email = email_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not email.has_object_write_permission(request)


def test_has_object_write_permission_owner(api_rf, email_factory):
    """
    Users should have write permissions on their own email addresses.
    """
    email = email_factory()

    api_rf.user = email.user
    request = api_rf.get('/')

    assert email.has_object_write_permission(request)


def test_set_primary(email_factory, user_factory):
    """
    Setting a user's email address as the primary address should mark
    all their other addresses as not primary.
    """
    user = user_factory()
    old_primary = email_factory(primary=True, user=user)
    new_primary = email_factory(user=user)

    new_primary.set_primary()

    user.refresh_from_db()
    new_primary.refresh_from_db()
    old_primary.refresh_from_db()

    assert user.email == new_primary.email
    assert new_primary.primary
    assert not old_primary.primary


def test_string_conversion(email_factory):
    """
    Converting an email address to a string should return the actual
    email address associated with the instance.
    """
    email = email_factory()

    assert str(email) == email.email


def test_verify_noop(email_factory, user_factory):
    """
    If the verified action is a noop, the email should be verified and
    that's it.
    """
    user = user_factory()

    # Create primary email
    email_factory(primary=True, user=user, verified=True)
    # Create unverified email
    email = email_factory(user=user, verified=False)

    email.verify()
    email.refresh_from_db()

    assert user.email_addresses.count() == 2
    assert not email.primary
    assert email.verified


def test_verify_replace_primary(email_factory, user_factory):
    """
    If the verified action is ``REPLACE_PRIMARY``, the email should
    replace the user's existing primary address when it is verified.
    """
    user = user_factory()

    # Create old primary
    email_factory(primary=True, user=user, verified=True)
    # Create unverified email
    email = email_factory(
        user=user,
        verified=False,
        verified_action=models.EmailAddress.REPLACE_PRIMARY)

    email.verify()
    email.refresh_from_db()

    assert user.email_addresses.count() == 1
    assert user.email_addresses.get() == email

    assert email.primary
    assert email.verified
