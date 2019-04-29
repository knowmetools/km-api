from unittest import mock

from account.models import User
from know_me import models


def test_has_object_read_permission_owner():
    """
    The owner of the subscription should have read permissions on the
    object.
    """
    user = User()
    request = mock.Mock(name="Mock Request")
    request.user = user

    subscription = models.Subscription(user=user)

    assert subscription.has_object_read_permission(request)


def test_has_object_read_permission_other():
    """
    Other users should not have read permission on the object.
    """
    subscription = models.Subscription(user=User())
    request = mock.Mock(name="Mock Request")
    request.user = User()

    assert not subscription.has_object_read_permission(request)


def test_has_object_write_permission_owner():
    """
    The owner of the subscription should have write permissions on the
    object.
    """
    user = User()
    request = mock.Mock(name="Mock Request")
    request.user = user

    subscription = models.Subscription(user=user)

    assert subscription.has_object_write_permission(request)


def test_has_object_write_permission_other():
    """
    Other users should not have write permission on the object.
    """
    subscription = models.Subscription(user=User())
    request = mock.Mock(name="Mock Request")
    request.user = User()

    assert not subscription.has_object_write_permission(request)


def test_string_conversion():
    """
    Converting a subscription to a string should return a user readable
    string containing the name of the user the subscription is
    associated with.
    """
    user_str = "John Doe"
    user = User()
    subscription = models.Subscription(user=user)
    expected = f"Know Me subscription for {user_str}"

    with mock.patch(
        "account.models.User.get_full_name", return_value=user_str
    ):
        assert str(subscription) == expected
