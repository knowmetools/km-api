from account import models


def test_create_email(user_factory):
    """
    Test creating an email.
    """
    email = models.EmailAddress.objects.create(
        email='test@example.com',
        user=user_factory())

    assert not email.verified


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
