import pytest
from django.http import Http404
from rest_framework import status
from rest_framework.reverse import reverse

from know_me import views, models
from know_me.serializers import subscription_serializers


def test_get_object_exists(api_rf, apple_subscription_factory):
    """
    If there is an Apple subscription for the requesting user, it should
    be returned.
    """
    subscription = apple_subscription_factory()
    api_rf.user = subscription.subscription.user
    request = api_rf.get('/')

    view = views.AppleSubscriptionView()
    view.request = request

    assert view.get_object() == subscription


def test_get_object_missing(api_rf, user_factory):
    """
    If the requesting user has no Apple subscription, an ``Http404``
    should be thrown for a ``GET`` request.
    """
    api_rf.user = user_factory()
    request = api_rf.get('/')

    view = views.AppleSubscriptionView()
    view.request = request

    with pytest.raises(Http404):
        view.get_object()


@pytest.mark.integration
def test_GET_existing_subscription(
        api_client,
        api_rf,
        apple_subscription_factory):
    """
    Sending a ``GET`` request to the endpoint as the owner of an
    existing Apple Subscription should return the details of the
    subscription.
    """
    subscription = apple_subscription_factory()

    api_client.force_authenticate(subscription.subscription.user)
    api_rf.user = subscription.subscription.user

    url = reverse('know-me:apple-subscription-detail')
    request = api_rf.get(url)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = subscription_serializers.AppleSubscriptionSerializer(
        subscription,
        context={'request': request},
    )

    assert response.data == serializer.data


@pytest.mark.integration
def test_PUT_existing_subscription(
        api_client,
        api_rf,
        apple_subscription_factory):
    """
    If the user already has an Apple subscription, it should be updated.
    """
    subscription = apple_subscription_factory(receipt_data='old receipt')
    user = subscription.subscription.user
    api_client.force_authenticate(user)
    api_rf.user = user

    data = {
        'receipt_data': 'new receipt',
    }

    url = reverse('know-me:apple-subscription-detail')
    request = api_rf.put(url, data)
    response = api_client.put(url, data)

    assert response.status_code == 200
    subscription.refresh_from_db()

    serializer = subscription_serializers.AppleSubscriptionSerializer(
        subscription,
        context={'request': request},
    )

    assert response.data == serializer.data
    assert models.SubscriptionAppleData.objects.count() == 1


@pytest.mark.integration
def test_PUT_new_subscription(api_client, api_rf, user_factory):
    """
    Sending a ``PUT`` request to the view should create a new Apple
    subscription for the requesting user.
    """
    user = user_factory()
    api_client.force_authenticate(user)
    api_rf.user = user

    data = {
        'receipt_data': 'receipt data',
    }

    url = reverse('know-me:apple-subscription-detail')
    request = api_rf.put(url, data)
    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_200_OK

    serializer = subscription_serializers.AppleSubscriptionSerializer(
        user.know_me_subscription.apple_data,
        context={'request': request},
    )

    assert response.data == serializer.data
