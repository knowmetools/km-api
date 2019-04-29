import hashlib
from unittest import mock

from know_me import models


def test_clean():
    """
    Cleaning a receipt should populate its hash field with the hash of
    its receipt data.
    """
    data = "foo"
    receipt = models.AppleReceipt(receipt_data=data)

    receipt.clean()

    assert receipt.receipt_data_hash == models.AppleReceipt.hash_data(data)


def test_has_object_read_permission():
    """
    The read permission check should be delegated to the parent
    subscription instance.
    """
    subscription = models.Subscription()
    receipt = models.AppleReceipt(subscription=subscription)
    request = mock.Mock(name="Mock Request")

    with mock.patch(
        "know_me.models.Subscription.has_object_read_permission"
    ) as mock_has_perm:
        result = receipt.has_object_read_permission(request)

    assert result == mock_has_perm.return_value
    assert mock_has_perm.call_args[0] == (request,)


def test_has_object_write_permission():
    """
    The write permission check should be delegated to the parent
    subscription instance.
    """
    subscription = models.Subscription()
    receipt = models.AppleReceipt(subscription=subscription)
    request = mock.Mock(name="Mock Request")

    with mock.patch(
        "know_me.models.Subscription.has_object_write_permission"
    ) as mock_has_perm:
        result = receipt.has_object_write_permission(request)

    assert result == mock_has_perm.return_value
    assert mock_has_perm.call_args[0] == (request,)


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


def test_hash_data():
    """
    The method should return the SHA256 hash of the provided data
    encoded as hexadecimal characters.
    """
    data = "foo"
    expected = hashlib.sha256(data.encode()).hexdigest()

    assert models.AppleReceipt.hash_data(data) == expected


def test_repr():
    """
    The repr method should return a string containing the information
    required to find the instance again for debugging purposes.
    """
    receipt = models.AppleReceipt()
    expected = f"<AppleReceipt: id='{receipt.id}'>"

    assert repr(receipt) == expected


def test_str():
    """
    Converting an Apple receipt to a string should return a string
    describing the Apple receipt and the subscription it is used for.
    """
    subscription = models.Subscription()
    subscription_str = "Mock Know Me Subscription"
    expected = f"Apple receipt for {subscription_str}"

    receipt = models.AppleReceipt(subscription=subscription)

    with mock.patch(
        "know_me.models.Subscription.__str__", return_value=subscription_str
    ):
        assert str(receipt) == expected
