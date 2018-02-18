def test_update_accessor_user(email_factory, km_user_accessor_factory):
    """
    When an email address matching an accessor that has no user is saved
    the accessor's user should be updated.
    """
    email = email_factory(is_verified=False)
    accessor = km_user_accessor_factory(email=email.email)

    email.is_verified = True
    email.save()

    accessor.refresh_from_db()

    assert accessor.user_with_access == email.user


def test_update_accessor_user_unverified_email(
        email_factory,
        km_user_accessor_factory):
    """
    If the email address is not verified, the accessor should not be
    updated.
    """
    email = email_factory(is_verified=False)
    accessor = km_user_accessor_factory(email=email.email)

    email.save()

    accessor.refresh_from_db()

    assert accessor.user_with_access is None


def test_update_accessor_with_user(
        email_factory,
        km_user_accessor_factory,
        user_factory):
    """
    If the accessor already has an associated user it should not be
    updated.
    """
    user = user_factory()
    email = email_factory(is_verified=True)
    accessor = km_user_accessor_factory(
        email=email.email,
        user_with_access=user)

    email.save()

    accessor.refresh_from_db()

    assert accessor.user_with_access == user
