from rest_framework import status

TRANSFER_URL = "/know-me/subscription/transfer/"


def test_transfer_anonymous(api_client, enable_premium_requirement):
    """
    Anonymous users should receive a 403 response if they attempt to
    initiate a transfer.
    """
    response = api_client.post(
        TRANSFER_URL, {"recipient_url": "fake@example.com"}
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_transfer_initiator_no_premium(
    api_client, enable_premium_requirement, subscription_factory, user_factory
):
    """
    If the user initiating the transfer does not have an active premium
    subscription, a 403 response should be returned.
    """
    # Assume Shawn and Juliet are two existing users, neither of whom
    # have premium subscriptions.
    password = "password"
    user1 = user_factory(first_name="Shawn", password=password)
    user2 = user_factory(first_name="Juliet", password=password)
    subscription_factory(is_active=False, user=user1)

    # If Shawn attempts to transfer his inactive subscription to Juliet,
    # he should receive a 403 response.
    api_client.log_in(user1.primary_email.email, password)
    response = api_client.post(
        TRANSFER_URL, {"recipient_email": user2.primary_email.email}
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_transfer_recipient_active_subscription(
    api_client, enable_premium_requirement, subscription_factory, user_factory
):
    """
    If the intended recipient has an active subscription, the transfer
    request should fail.
    """
    # Assume Shawn and Juliet are two existing users, both with active
    # premium subscriptions.
    password = "password"
    user1 = user_factory(
        first_name="Shawn", has_premium=True, password=password
    )
    user2 = user_factory(
        first_name="Shawn", has_premium=True, password=password
    )

    # If Shawn tries to transfer his premium subscription to Juliet, he
    # should receive an error because Juliet already has a subscription.
    api_client.log_in(user1.primary_email.email, password)
    response = api_client.post(
        TRANSFER_URL, {"recipient_email": user2.primary_email.email}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "non_field_errors": [
            "The intended recipient already has an active premium "
            "subscription."
        ]
    }


def test_transfer_recipient_apple_receipt(
    api_client, apple_receipt_factory, enable_premium_requirement, user_factory
):
    """
    If the intended recipient has an Apple receipt associated with their
    account, they should not be able to receive a subscription transfer,
    even if their subscription is inactive.
    """
    # Assume Shawn is an existing user with an active premium
    # subscription...
    password = "password"
    user1 = user_factory(
        first_name="Shawn", has_premium=True, password=password
    )

    # ...and Juliet is a user with an inactive premium subscription but
    # who has an Apple receipt tied to her account.
    user2 = user_factory(first_name="Juliet", password=password)
    apple_receipt_factory(
        subscription__is_active=False, subscription__user=user2
    )

    # If Shawn tries to transfer his premium subscription to Juliet, the
    # transfer should fail.
    api_client.log_in(user1.primary_email.email, password)
    response = api_client.post(
        TRANSFER_URL, {"recipient_email": user2.primary_email.email}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "non_field_errors": [
            "The intended recipient has an Apple subscription that must be "
            "removed before they can accept a transfer."
        ]
    }


def test_transfer_recipient_no_subscription(
    api_client, enable_premium_requirement, subscription_factory, user_factory
):
    """
    If we have two users, one who has an active subscription and one who
    does not, the user with the active subscription should be able to
    transfer their subscription to the user without one.
    """
    # Assume Shawn and Juliet are two existing users. Shawn has an
    # active premium subscription.
    password = "password"
    user1 = user_factory(
        first_name="Shawn", has_premium=True, password=password
    )
    user2 = user_factory(first_name="Juliet", password=password)

    # If Shawn logs in, he should be able to transfer his subscription
    # to Juliet.
    api_client.log_in(user1.primary_email.email, password)
    transfer_response = api_client.post(
        TRANSFER_URL, {"recipient_email": user2.primary_email.email}
    )

    assert transfer_response.status_code == status.HTTP_201_CREATED

    # Shawn should no longer be a premium user.
    assert not api_client.user_has_premium

    # Juliet should be a premium user.
    api_client.log_in(user2.primary_email.email, password)

    assert api_client.user_has_premium
