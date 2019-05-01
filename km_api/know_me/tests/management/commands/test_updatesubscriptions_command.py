import datetime
from unittest import mock

import pytest
from django.utils import timezone

from know_me import models, subscriptions
from know_me.management.commands.updatesubscriptions import Command

PREMIUM_PRODUCT_CODE = "premium"
RENEWAL_WINDOW = datetime.timedelta(hours=1)


@pytest.fixture
def mock_subscription_qs():
    """
    Fixture to mock querysets interacting with subscriptions.
    """
    mock_qs = mock.Mock(spec=models.Subscription.objects)
    mock_qs.filter.return_value = mock_qs

    with mock.patch("know_me.models.Subscription.objects", new=mock_qs):
        yield mock_qs


@pytest.fixture(autouse=True)
def set_know_me_premium_product_codes(settings):
    """
    Fixture to automatically set the product code for Know Me Premium.
    """
    settings.APPLE_PRODUCT_CODES["KNOW_ME_PREMIUM"] = [PREMIUM_PRODUCT_CODE]


def test_deactivate_orphan_subscriptions(mock_subscription_qs):
    """
    Subscriptions that have no receipts activating them should be
    deactivated.
    """
    mock_filtered_qs = mock.Mock(name="Mock Subscription Queryset")
    mock_subscription_qs.filter.return_value = mock_filtered_qs

    result = Command.deactivate_orphan_subscriptions()

    assert mock_subscription_qs.filter.call_args[1] == {
        "apple_receipt__isnull": True,
        "is_active": True,
    }
    assert mock_filtered_qs.update.call_args[1] == {"is_active": False}
    assert result == mock_filtered_qs.update.return_value


@mock.patch("know_me.management.commands.updatesubscriptions.timezone.now")
@mock.patch(
    "know_me.management.commands.updatesubscriptions.Command.deactivate_orphan_subscriptions"  # noqa
)
@mock.patch(
    "know_me.management.commands.updatesubscriptions.Command.update_apple_subscriptions"  # noqa
)
def test_handle(mock_update_apple, mock_deactivate_orphans, mock_now):
    """
    The entry point into the command should execute the methods used to
    deactivate orphan subscriptions and update Apple subscriptions.
    """
    now = timezone.now()
    mock_now.return_value = now

    command = Command()
    command.handle()

    assert mock_deactivate_orphans.call_count == 1
    assert mock_update_apple.call_args[0] == (now, command.RENEWAL_WINDOW)


def test_update_apple_subscriptions_error(
    mock_apple_receipt_qs, mock_subscription_qs
):
    """
    If there is an error when trying to update a receipt's information,
    its parent subscription should be marked as expired.
    """
    now = timezone.now()
    receipt = mock.Mock(name="Mock Receipt")
    receipt.update_info.side_effect = subscriptions.ReceiptException("foo")
    mock_apple_receipt_qs.filter.return_value = [receipt]

    command = Command()
    command.update_apple_subscriptions(now, RENEWAL_WINDOW)

    assert mock_apple_receipt_qs.filter.call_args[1] == {
        "expiration_time__lte": now + RENEWAL_WINDOW
    }
    assert receipt.update_info.call_count == 1
    assert mock_subscription_qs.filter.call_args[1] == {
        "apple_receipt": receipt
    }
    assert mock_subscription_qs.update.call_args[1] == {"is_active": False}


def test_update_apple_subscriptions_expiring(
    mock_apple_receipt_qs, mock_subscription_qs
):
    """
    If an Apple receipt's expiration time has passed, its parent
    subscription should be deactivated.
    """
    now = timezone.now()
    receipt = mock.Mock(name="Mock Receipt")
    receipt.expiration_time = now - datetime.timedelta(hours=1)
    mock_apple_receipt_qs.filter.return_value = [receipt]

    command = Command()
    command.update_apple_subscriptions(now, RENEWAL_WINDOW)

    assert mock_apple_receipt_qs.filter.call_args[1] == {
        "expiration_time__lte": now + RENEWAL_WINDOW
    }
    assert receipt.update_info.call_count == 1
    assert mock_subscription_qs.filter.call_args[1] == {
        "apple_receipt": receipt
    }
    assert mock_subscription_qs.update.call_args[1] == {"is_active": False}


def test_update_apple_subscriptions_renewed(
    mock_apple_receipt_qs, mock_subscription_qs
):
    """
    If a receipt that had previously expired becomes active again, the
    parent subscription should be activated.
    """
    now = timezone.now()
    receipt = mock.Mock(name="Mock Receipt")
    receipt.expiration_time = now + datetime.timedelta(hours=1)
    mock_apple_receipt_qs.filter.return_value = [receipt]

    command = Command()
    command.update_apple_subscriptions(now, RENEWAL_WINDOW)

    assert mock_apple_receipt_qs.filter.call_args[1] == {
        "expiration_time__lte": now + RENEWAL_WINDOW
    }
    assert receipt.update_info.call_count == 1
    assert mock_subscription_qs.filter.call_args[1] == {
        "apple_receipt": receipt
    }
    assert mock_subscription_qs.update.call_args[1] == {"is_active": True}


def test_update_apple_subscriptions_still_valid(
    mock_apple_receipt_qs, mock_subscription_qs
):
    """
    If an Apple receipt successfully updates its information through the
    Apple store, it should be saved.
    """
    now = timezone.now()
    receipts = []
    for i in range(10):
        receipt = mock.Mock(name=f"Mock Receipt {i}")
        receipt.expiration_time = now + datetime.timedelta(minutes=1)
        receipts.append(receipt)

    mock_apple_receipt_qs.filter.return_value = receipts

    command = Command()
    command.update_apple_subscriptions(now, RENEWAL_WINDOW)

    assert mock_apple_receipt_qs.filter.call_args[1] == {
        "expiration_time__lte": now + RENEWAL_WINDOW
    }

    for receipt in receipts:
        assert receipt.update_info.call_count == 1
        assert receipt.save.call_count == 1
