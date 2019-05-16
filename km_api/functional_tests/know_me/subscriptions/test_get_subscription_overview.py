from rest_framework import status

from test_utils import serialized_time


URL = "/know-me/subscription/"


def test_get_subscription_anonymous(api_client):
    """
    Anonymous users should receive a 403 response if they attempt to access
    this endpoint.
    """
    response = api_client.get(URL)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_subscription_apple_receipt(
    api_client, apple_receipt_factory, user_factory
):
    """
    If the requesting user has an Apple receipt as their payment source
    for a premium subscription, info about it should be returned by the
    overview endpoint.
    """
    # Assume Elijah is an existing user with an Apple receipt.
    password = "password"
    user = user_factory(first_name="Elijah", password=password)
    apple_receipt = apple_receipt_factory(
        subscription__is_active=True, subscription__user=user
    )

    # Elijah should now be able to get an overview of his subscription.
    api_client.log_in(user.primary_email.email, password)
    response = api_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "apple_receipt": {
            "expiration_time": serialized_time(apple_receipt.expiration_time)
        },
        "is_active": True,
        "is_legacy_subscription": False,
    }


def test_get_subscription_legacy(
    api_client, user_factory, subscription_factory
):
    """
    If the requesting user has a legacy subscription, the subscription
    overview should include a flag indicating that.
    """
    # Assume Matt is an existing user with a legacy subscription.
    password = "password"
    user = user_factory(first_name="Matt", password="password")
    subscription = subscription_factory(is_legacy_subscription=True, user=user)

    # If he gets an overview of his subscriptions, he should see a flag
    # indicating he has a legacy subscription.
    api_client.log_in(user.primary_email.email, password)
    response = api_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "apple_receipt": None,
        "is_active": subscription.is_active,
        "is_legacy_subscription": True,
    }


def test_get_subscription_non_existent(api_client, user_factory):
    """
    If the requesting user does not have a subscription, they should
    receive a 404 response.
    """
    # Assume Anders is an existing user without a subscription.
    password = "password"
    user = user_factory(first_name="Anders", password=password)
    api_client.log_in(user.primary_email.email, password)

    # If he attempts to view the details of his non-existent
    # subscription, he should receive a 404 response.
    response = api_client.get(URL)

    assert response.status_code == status.HTTP_404_NOT_FOUND
