from know_me import models


def test_unverified_legacy(
    email_factory, km_user_factory, legacy_user_factory
):
    """
    Saving an email address that is not verified should not do anything.
    """
    email = email_factory(is_verified=False)
    legacy_user_factory(email=email.email)

    # The registration signal is not sent, so we need to manually create
    # a Know Me user.
    km_user_factory(user=email.user)

    email.save()

    assert not email.user.km_user.is_legacy_user


def test_verify_email(email_factory, km_user_factory):
    """
    If there is no legacy user matching the email address, no action
    should be taken.
    """
    email = email_factory(is_verified=False)

    # The registration signal is not sent, so we need to manually create
    # a Know Me user.
    km_user_factory(user=email.user)

    email.is_verified = True
    email.save()

    assert not email.user.km_user.is_legacy_user


def test_verify_legacy_email(
    email_factory, km_user_factory, legacy_user_factory
):
    """
    If a user verifies an email address that corresponds to a legacy
    user, that user should be marked accordingly and the legacy user
    should be deleted.
    """
    email = email_factory(is_verified=False)
    legacy_user_factory(email=email.email)

    # The registration signal is not sent, so we need to manually create
    # a Know Me user.
    km_user_factory(user=email.user)

    email.is_verified = True
    email.save()

    assert email.user.km_user.is_legacy_user
    assert models.LegacyUser.objects.count() == 0
