from unittest import mock

from know_me import models
from know_me.management.commands.updatelegacyusers import Command


def test_find_legacy_users_match_email(email_factory, legacy_user_factory):
    """
    If the email address of a legacy user matches a verified email, the
    Know Me user corresponding to the owner of the email address should
    be marked as a legacy user.
    """
    email_inst = email_factory(
        is_verified=True, user__registration_signal__send=True
    )
    legacy_user_factory(email=email_inst.email)

    command = Command()
    command.find_legacy_users()
    email_inst.refresh_from_db()

    assert email_inst.user.km_user.is_legacy_user
    assert not models.LegacyUser.objects.exists()


def test_find_legacy_users_match_email_unverified(
    email_factory, legacy_user_factory
):
    """
    If a legacy email matches a current user's email but the email is
    unverified, no action should be taken.
    """
    email_inst = email_factory(
        is_verified=False, user__registration_signal__send=True
    )
    legacy_user_factory(email=email_inst.email)

    command = Command()
    command.find_legacy_users()
    email_inst.refresh_from_db()

    assert not email_inst.user.km_user.is_legacy_user


@mock.patch(
    "know_me.management.commands.updatelegacyusers.Command.find_legacy_users"
)
@mock.patch(
    "know_me.management.commands.updatelegacyusers.Command.update_legacy_subscriptions"  # noqa
)
def test_handle(mock_update, mock_find):
    """
    The entry point into the command should delegate to the methods
    responsible for each task in the command.
    """
    command = Command()
    command.handle()

    assert mock_find.call_count == 1
    assert mock_update.call_count == 1


def test_update_legacy_subscriptions_clear_invalid(
    km_user_factory, subscription_factory
):
    """
    If a user has a legacy subscription but is not a legacy user, their
    subscription should be deactivated when the command is run.
    """
    subscription = subscription_factory(
        is_legacy_subscription=True, is_active=True
    )
    km_user_factory(is_legacy_user=False, user=subscription.user)

    command = Command()
    command.update_legacy_subscriptions()

    subscription.refresh_from_db()

    assert not subscription.is_legacy_subscription
    assert not subscription.is_active


def test_update_legacy_subscriptions_grant_subscription(km_user_factory):
    """
    If a Know Me user is marked as a legacy user, their subscription
    should be active and the flag indicating it is a legacy subscription
    should be set.
    """
    km_user = km_user_factory(is_legacy_user=True)

    command = Command()
    command.update_legacy_subscriptions()

    subscription = km_user.user.know_me_subscription

    assert subscription.is_legacy_subscription
    assert subscription.is_active


def test_update_legacy_subscriptions_grant_subscription_exists(
    km_user_factory, subscription_factory
):
    """
    If a Know Me user is marked as a legacy user and they already have a
    subscription instance, their subscription should be updated to be
    active and marked as a legacy subscription.
    """
    km_user = km_user_factory(is_legacy_user=True)
    subscription = subscription_factory(
        is_legacy_subscription=False, is_active=False, user=km_user.user
    )

    command = Command()
    command.update_legacy_subscriptions()

    subscription.refresh_from_db()

    assert subscription.is_legacy_subscription
    assert subscription.is_active


def test_update_legacy_subscriptions_not_legacy_user(km_user_factory):
    """
    If a Know Me user is not a legacy user, their subscription should
    not be modified.
    """
    km_user = km_user_factory(is_legacy_user=False)

    command = Command()
    command.update_legacy_subscriptions()

    assert not hasattr(km_user.user, "know_me_subscription")
