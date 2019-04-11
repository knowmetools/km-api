import datetime
import hashlib
from unittest import mock

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from know_me import models


def test_clean():
    """
    Cleaning the model should populate the receipt data hash field.
    """
    receipt_data = "base64-encoded-receipt-data"
    data = models.SubscriptionAppleData(receipt_data=receipt_data)
    expected = hashlib.sha256(receipt_data.encode()).hexdigest()

    data.clean()

    assert data.receipt_data_hash == expected


def test_has_object_read_permission_owner(api_rf, apple_subscription_factory):
    """
    The owner of the subscription should have read access to it.
    """
    subscription = apple_subscription_factory()
    api_rf.user = subscription.subscription.user
    request = api_rf.get("/")

    assert subscription.has_object_read_permission(request)


def test_has_object_read_permission_other(
    api_rf, apple_subscription_factory, user_factory
):
    """
    If the requesting user does not own the subscription, they should
    not be granted read access.
    """
    subscription = apple_subscription_factory()
    api_rf.user = user_factory()
    request = api_rf.get("/")

    assert not subscription.has_object_read_permission(request)


def test_has_object_write_permission_owner(api_rf, apple_subscription_factory):
    """
    The owner of the subscription should have write access to it.
    """
    subscription = apple_subscription_factory()
    api_rf.user = subscription.subscription.user
    request = api_rf.get("/")

    assert subscription.has_object_write_permission(request)


def test_has_object_write_permission_other(
    api_rf, apple_subscription_factory, user_factory
):
    """
    If the requesting user does not own the subscription, they should
    not be granted write access.
    """
    subscription = apple_subscription_factory()
    api_rf.user = user_factory()
    request = api_rf.get("/")

    assert not subscription.has_object_write_permission(request)


def test_save_update_base_subscription_active(apple_subscription_factory):
    """
    If the expiration date of the Apple subscription has not passed, the
    base subscription should be made active when the Apple subscription
    is saved.
    """
    future_time = timezone.now() + datetime.timedelta(days=1)

    apple_subscription = apple_subscription_factory()
    apple_subscription.expiration_time = future_time
    apple_subscription.subscription.is_active = False

    with mock.patch.object(
        apple_subscription.subscription, "save"
    ) as mock_save:
        apple_subscription.save()

    assert apple_subscription.subscription.is_active
    assert mock_save.call_count == 1


def test_save_update_base_subscription_expired(apple_subscription_factory):
    """
    If the expiration date of the Apple subscription has passed, the
    base subscription should be made inactive when the Apple
    subscription is saved.
    """
    past_time = timezone.now() - datetime.timedelta(days=1)

    apple_subscription = apple_subscription_factory()
    apple_subscription.expiration_time = past_time
    apple_subscription.subscription.is_active = True

    with mock.patch.object(
        apple_subscription.subscription, "save"
    ) as mock_save:
        apple_subscription.save()

    assert not apple_subscription.subscription.is_active
    assert mock_save.call_count == 1


def test_string_conversion(apple_subscription_factory):
    """
    Converting an instance to a string should return a user readable
    string containing information about the parent subscription.
    """
    data = apple_subscription_factory()
    expected = "Apple subscription data for the {subscription}".format(
        subscription=data.subscription
    )

    assert str(data) == expected


def test_validate_unique_different_receipts(apple_subscription_factory):
    """
    If there are no other apple subscriptions with the instance's
    receipt data, the unique validation should pass.
    """
    apple_subscription_factory(receipt_data="data-1")

    apple_data = models.SubscriptionAppleData(receipt_data="data-2")
    apple_data.validate_unique()


def test_validate_unique_duplicate_receipt_data(apple_subscription_factory):
    """
    If there is an existing Apple receipt with the same receipt data as
    the instance, the unique validation should fail.
    """
    existing_data = apple_subscription_factory()
    new_data = models.SubscriptionAppleData(
        receipt_data=existing_data.receipt_data
    )
    new_data.clean()

    with pytest.raises(ValidationError):
        new_data.validate_unique()
