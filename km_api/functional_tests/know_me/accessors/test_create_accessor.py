from rest_framework import status


URL = "/know-me/users/accessors/"


def test_create_anonymous(api_client, km_user_factory):
    """
    Anonymous users should receive a 403 response if they try to create
    an accessor.
    """
    response = api_client.post(URL, {"email": "test@example.com"})

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_as_non_premium_user(api_client, km_user_factory):
    """
    Non-premium users should receive a 403 response if they try to add a
    new accessor.
    """
    # If Iris is a non-premium user...
    password = "password"
    km_user = km_user_factory(
        user__first_name="Iris",
        user__has_premium=False,
        user__password="password",
    )
    api_client.log_in(km_user.user.primary_email.email, password)

    # ...and she attempts to add an accessor, then she should receive a
    # permission denied error.
    data = {"email": "share@example.com"}
    response = api_client.post(URL, data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_as_premium_user(api_client, km_user_factory):
    """
    Premium users should be able to create accessors to share their
    Know Me user with others.
    """
    # Assume Barry is an existing user with a premium subscription.
    password = "password"
    km_user = km_user_factory(
        user__first_name="Barry",
        user__has_premium=True,
        user__password=password,
    )
    api_client.log_in(km_user.user.primary_email.email, password)

    # He should be able to share his account with another user.
    data = {"email": "share@example.com"}
    response = api_client.post(URL, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == data["email"]
