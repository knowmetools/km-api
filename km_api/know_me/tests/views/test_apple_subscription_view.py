import pytest
from django.http import Http404
from rest_framework import status
from rest_framework.reverse import reverse

from know_me import views
from know_me.serializers import subscription_serializers


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


@pytest.mark.integration
def test_GET_existing_subscription(
    api_client, api_rf, apple_subscription_factory
):
    """
    Sending a ``GET`` request to the endpoint as the owner of an
    existing Apple Subscription should return the details of the
    subscription.
    """
    subscription = apple_subscription_factory()

    api_client.force_authenticate(subscription.subscription.user)
    api_rf.user = subscription.subscription.user

    url = reverse("know-me:apple-subscription-detail")
    request = api_rf.get(url)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = subscription_serializers.AppleSubscriptionSerializer(
        subscription, context={"request": request}
    )

    assert response.data == serializer.data
