

def test_update_accessor_duplicate(
        email_factory,
        km_user_factory,
        km_user_accessor_factory,
        user_factory):
    """
    If a user is granted access through two emails, one verified and one
    unverified, then when they verify the second email, a duplicate
    accessor should not be created.
    """
    km_user = km_user_factory()

    user = user_factory()
    e1 = email_factory(is_verified=True, user=user)
    e2 = email_factory(is_verified=False, user=user)

    km_user_accessor_factory(
        email=e1.email,
        km_user=km_user,
        user_with_access=user)
    accessor = km_user_accessor_factory(email=e2.email, km_user=km_user)

    e2.is_verified = True
    e2.save()

    assert not km_user.km_user_accessors.filter(id=accessor.id).exists()


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
