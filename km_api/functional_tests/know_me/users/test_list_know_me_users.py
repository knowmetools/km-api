import pytest
from rest_framework import status

from functional_tests import serialization_helpers

LIST_URL = "/know-me/users/"


@pytest.mark.parametrize("is_premium", [True, False])
def test_km_user_premium_flag(api_client, is_premium, km_user_factory):
    """
    The response from the Know Me user list should include a boolean
    property indicating if each user is a premium user.
    """
    # Given a Know Me user...
    password = "password"
    km_user = km_user_factory(
        user__has_premium=is_premium, user__password=password
    )
    api_client.log_in(km_user.user.primary_email.email, password)

    # If they list all Know Me users...
    response = api_client.get(LIST_URL)

    # The response should indicate if the Know Me user is a premium
    # user.
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["is_premium_user"] == is_premium


def test_list_anonymous(api_client):
    """
    Anonymous users should receive a 403 response.
    """
    response = api_client.get(LIST_URL)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_list_own_first(
    api_client, km_user_accessor_factory, km_user_factory, user_factory
):
    """
    If the requesting user has a Know Me user and is granted access to
    additional Know Me users via accessors, the user's own Know Me user
    should be listed first.
    """
    # Given an existing user...
    password = "password"
    user = user_factory(password=password)
    api_client.log_in(user.primary_email.email, password)

    # ...who is granted access to another user...
    accessor = km_user_accessor_factory(
        is_accepted=True,
        km_user__user__has_premium=True,
        user_with_access=user,
    )

    # ...and has their own Know Me user...
    km_user = km_user_factory(user=user)

    # ...then when they list the users they have access to, their own
    # user should be listed first.
    response = api_client.get(LIST_URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == serialization_helpers.km_user_list(
        [km_user, accessor.km_user],
        lambda km: km.user == user,
        api_client.build_full_url,
    )


def test_list_own_no_premium(api_client, km_user_factory):
    """
    If a user does not have premium, the list should still include their
    own Know Me user.
    """
    # Given an existing Know Me user...
    password = "password"
    km_user = km_user_factory(user__password=password)
    api_client.log_in(km_user.user.primary_email.email, password)

    # ...they should be able to list their own Know Me user
    response = api_client.get(LIST_URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == serialization_helpers.km_user_list(
        [km_user],
        # All users are owned by the requesting user.
        lambda _: True,
        api_client.build_full_url,
    )


def test_list_shared_with_premium(
    api_client, km_user_accessor_factory, user_factory
):
    """
    If the requesting user has been granted access to another profile
    and the profile's owner has an active premium subscription, the user
    should be listed.
    """
    password = "password"
    user = user_factory(password="password")
    accessor = km_user_accessor_factory(
        is_accepted=True,
        km_user__user__has_premium=True,
        user_with_access=user,
    )

    api_client.log_in(user.primary_email.email, password)
    response = api_client.get(LIST_URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == serialization_helpers.km_user_list(
        [accessor.km_user],
        # None of the users are owned by the requesting user
        lambda _: False,
        api_client.build_full_url,
    )


def test_list_shared_without_premium(
    api_client, km_user_accessor_factory, user_factory
):
    """
    If a user has access to a profile through an accessor but the
    profile's owner does not have an active premium subscription, the
    shared user should not be listed.
    """
    password = "password"
    user = user_factory(password="password")
    km_user_accessor_factory(is_accepted=True, user_with_access=user)

    api_client.log_in(user.primary_email.email, password)
    response = api_client.get(LIST_URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
