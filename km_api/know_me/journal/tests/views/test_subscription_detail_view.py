import pytest
from django.http import Http404

from know_me import views
from know_me.serializers import subscription_serializers


def test_get_object(api_rf, subscription_factory):
    """
    If the requesting user has a subscription instance, it should be
    returned.
    """
    subscription = subscription_factory()
    api_rf.user = subscription.user

    view = views.SubscriptionDetailView()
    view.request = api_rf.get("/")

    assert view.get_object() == subscription


def test_get_object_non_existent(api_rf, user_factory):
    """
    If the requesting user does not have a subscription instance, an
    ``Http404`` exception should be raised.
    """
    api_rf.user = user_factory()

    view = views.SubscriptionDetailView()
    view.request = api_rf.get("/")

    with pytest.raises(Http404):
        view.get_object()


def test_get_serializer_class():
    """
    Test which serializer class is used by the view.
    """
    view = views.SubscriptionDetailView()
    expected = subscription_serializers.SubscriptionSerializer

    assert view.get_serializer_class() == expected
