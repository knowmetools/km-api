from rest_framework import status


URL = "/know-me/subscription/apple/"


def test_delete_anonymous(api_client):
    """
    If an anonymous user attempts to access the view they should receive
    a 403 response.
    """
    response = api_client.delete(URL)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_apple_subscription(
    api_client, apple_receipt_factory, user_factory
):
    """
    A user should be able to remove an Apple receipt they have
    previously added to their account.
    """
    # Assume Matt is an existing user with an Apple receipt added to his
    # account.
    password = "password"
    user = user_factory(first_name="Matt", has_premium=True, password=password)
    apple_receipt_factory(subscription=user.know_me_subscription)

    # If he deletes his Apple receipt, his premium subscription should be
    # deactivated.
    api_client.log_in(user.primary_email.email, password)
    response = api_client.delete(URL)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not api_client.user_has_premium


def test_delete_no_apple_subscription(api_client, user_factory):
    """
    If the requesting user does not have an Apple receipt uploaded, a
    404 response should be returned.
    """
    # Assume Ashley is an existing user without a subscription.
    password = "password"
    user = user_factory(
        first_name="Ashley", has_premium=True, password=password
    )
    api_client.log_in(user.primary_email.email, password)

    # If she attempts to delete her non-existent Apple receipt, she
    # should receive a 404 response.
    response = api_client.delete(URL)

    assert response.status_code == status.HTTP_404_NOT_FOUND
