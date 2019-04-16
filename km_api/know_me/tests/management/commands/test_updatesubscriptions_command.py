import datetime

import pytest
from django.utils import timezone

from know_me.management.commands.updatesubscriptions import Command


PREMIUM_PRODUCT_CODE = "premium"


@pytest.fixture(autouse=True)
def set_know_me_premium_product_codes(settings):
    """
    Fixture to automatically set the product code for Know Me Premium.
    """
    settings.APPLE_PRODUCT_CODES["KNOW_ME_PREMIUM"] = [PREMIUM_PRODUCT_CODE]


def test_handle_no_subscriptions(db):
    """
    If there are no subscriptions, ``handle`` should succeed without
    doing anything.
    """
    command = Command()
    command.handle()


def test_handle_expiring_apple_subscription(
    apple_receipt_client, apple_subscription_factory
):
    """
    If an Apple subscription's expiration time has passed, then its
    parent subscription should be marked as inactive when the command is
    run.
    """
    expires = timezone.now().replace(microsecond=0) - datetime.timedelta(
        days=30
    )
    apple_data = apple_subscription_factory(subscription__is_active=True)

    apple_receipt_client.enqueue_status(
        apple_data.receipt_data,
        {
            "status": 0,
            "latest_receipt_info": [
                {
                    "expires_data_ms": str(int(expires.timestamp() * 1000)),
                    "product_id": PREMIUM_PRODUCT_CODE,
                }
            ],
        },
    )

    command = Command()
    command.handle()
    apple_data.refresh_from_db()

    assert not apple_data.subscription.is_active


def test_handle_renewed_apple_subscription(
    apple_receipt_client, apple_subscription_factory
):
    """
    If an Apple subscription has lapsed and rendered its parent
    subscription inactive, then running the command after the Apple
    subscription has been renewed should activate the parent
    subscription.
    """
    new_expires = timezone.now().replace(microsecond=0) + datetime.timedelta(
        days=30
    )
    apple_data = apple_subscription_factory(
        expiration_time=timezone.now() + Command.EXPIRATION_WINDOW,
        subscription__is_active=False,
    )

    apple_receipt_client.enqueue_status(
        apple_data.receipt_data,
        {
            "status": 0,
            "latest_receipt_info": [
                {
                    "expires_date_ms": str(
                        int(new_expires.timestamp() * 1000)
                    ),
                    "product_id": PREMIUM_PRODUCT_CODE,
                }
            ],
        },
    )

    command = Command()
    command.handle()
    apple_data.refresh_from_db()

    assert apple_data.expiration_time == new_expires
    assert apple_data.subscription.is_active


def test_handle_still_expired_apple_subscription(
    apple_receipt_client, apple_subscription_factory
):
    """
    If an Apple receipt has already expired and the subscription has
    been marked as inactive, then running the command should keep the
    subscription inactive.
    """
    apple_data = apple_subscription_factory(
        expiration_time=timezone.now() - Command.EXPIRATION_WINDOW,
        subscription__is_active=False,
    )

    apple_receipt_client.enqueue_status(
        apple_data.receipt_data, {"status": 21010}
    )

    command = Command()
    command.handle()
    apple_data.refresh_from_db()

    assert not apple_data.subscription.is_active


def test_handle_subscription_no_receipt(subscription_factory):
    """
    If there is an active subscription without any receipt data (ie the
    receipt data got deleted), it should be set to inactive when the
    command is run.
    """
    subscription = subscription_factory(is_active=True)

    command = Command()
    command.handle()
    subscription.refresh_from_db()

    assert not subscription.is_active
