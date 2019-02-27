import pytest
from django.http import Http404

from know_me import views


def test_get_object_exists(api_rf, apple_subscription_factory):
    """
    If there is an Apple subscription for the requesting user, it should
    be returned.
    """
    subscription = apple_subscription_factory()
    api_rf.user = subscription.subscription.user
    request = api_rf.get("/")

    view = views.AppleSubscriptionView()
    view.request = request

    assert view.get_object() == subscription


def test_get_object_missing(api_rf, user_factory):
    """
    If the requesting user has no Apple subscription, an ``Http404``
    should be thrown for a ``GET`` request.
    """
    api_rf.user = user_factory()
    request = api_rf.get("/")

    view = views.AppleSubscriptionView()
    view.request = request

    with pytest.raises(Http404):
        view.get_object()
