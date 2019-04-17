import pytest
from django.core.exceptions import ValidationError

from know_me import models
from test_utils import receipt_data_hash


def test_clean_different_original_and_latest_data():
    """
    If the latest receipt data and most recent receipt data are
    different then cleaning the model shouldn't affect those fields.
    """
    r1 = "foo"
    r2 = "bar"
    data = models.SubscriptionAppleData(
        latest_receipt_data=r1, receipt_data=r2
    )

    data.clean()

    assert data.latest_receipt_data == r1
    assert data.receipt_data == r2


def test_clean_no_latest_receipt_data():
    """
    If no latest receipt data is set, cleaning the model should set the
    latest receipt data to the original receipt data.
    """
    receipt_data = "foo"
    data = models.SubscriptionAppleData(receipt_data=receipt_data)

    data.clean()

    assert data.latest_receipt_data == receipt_data


def test_clean_latest_receipt_data_hash():
    """
    Cleaning the model should populate the latest receipt data hash
    field.
    """
    receipt_data = "base64-encoded-receipt-data"
    data = models.SubscriptionAppleData(latest_receipt_data=receipt_data)
    expected = receipt_data_hash(receipt_data)

    data.clean()

    assert data.latest_receipt_data_hash == expected


def test_clean_receipt_data_hash():
    """
    Cleaning the model should populate the receipt data hash field.
    """
    receipt_data = "base64-encoded-receipt-data"
    data = models.SubscriptionAppleData(receipt_data=receipt_data)
    expected = receipt_data_hash(receipt_data)

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


def test_validate_unique_duplicate_latest_receipt_data(
    apple_subscription_factory
):
    """
    If there is an existing Apple receipt with the same latest receipt
    data, the unique validation should fail.
    """
    existing_receipt = apple_subscription_factory(
        latest_receipt_data="foo", receipt_data="bar"
    )
    new_receipt = models.SubscriptionAppleData(
        latest_receipt_data=existing_receipt.latest_receipt_data
    )
    new_receipt.clean()

    with pytest.raises(ValidationError):
        new_receipt.validate_unique()


def test_validate_unique_duplicate_latest_to_original(
    apple_subscription_factory
):
    """
    If there is an existing Apple receipt whose original receipt data
    matches the instance's latest receipt data, validation should fail.
    """
    existing_receipt = apple_subscription_factory(
        latest_receipt_data="foo", receipt_data="bar"
    )
    new_receipt = models.SubscriptionAppleData(
        latest_receipt_data=existing_receipt.receipt_data
    )
    new_receipt.clean()

    with pytest.raises(ValidationError):
        new_receipt.validate_unique()


def test_validate_unique_duplicate_original_receipt_data(
    apple_subscription_factory
):
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


def test_validate_unique_duplicate_original_to_latest(
    apple_subscription_factory
):
    """
    If there is an existing Apple receipt whose latest receipt data
    matches the instance's original receipt data, validation should
    fail.
    """
    existing_receipt = apple_subscription_factory(
        latest_receipt_data="foo", receipt_data="bar"
    )
    new_receipt = models.SubscriptionAppleData(
        latest_receipt_data="baz",
        receipt_data=existing_receipt.latest_receipt_data,
    )
    new_receipt.clean()

    with pytest.raises(ValidationError):
        new_receipt.validate_unique()
