from rest_framework import status

from functional_tests import serialization_helpers


URL = "/know-me/users/accessors/"


def test_list_anonymous(api_client):
    """
    If an anonymous user attempts to access the view, they should
    receive a 403 response.

    Regression test for #325
    """
    response = api_client.get(URL)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_list_accessors(
    api_client, km_user_accessor_factory, km_user_factory, user_factory
):
    """
    If an authenticated user accesses this endpoint, it should list all
    the accessors granting access to their Know Me user.
    """
    # Given an existing Know Me user...
    password = "password"
    km_user = km_user_factory(user__has_premium=True, user__password=password)
    api_client.log_in(km_user.user.primary_email.email, password)

    # ...and some accessors granting access to that user...
    accessor1 = km_user_accessor_factory(is_accepted=True, km_user=km_user)
    accessor2 = km_user_accessor_factory(
        is_accepted=False, km_user=km_user, user_with_access=user_factory()
    )

    # ...then the accessor list view should list those accessors.
    response = api_client.get(URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == list(
        map(
            lambda accessor: serialization_helpers.km_user_accessor(
                accessor, api_client.build_full_url
            ),
            [accessor1, accessor2],
        )
    )


def test_list_accessors_non_premium(
    api_client, enable_premium_requirement, km_user_factory
):
    """
    If a user does not have a premium subscription, they should receive
    a 403 response if they try to list the accessors granting access to
    their account.
    """
    # Given John is an existing Know Me user without a premium
    # subscription...
    password = "password"
    km_user = km_user_factory(
        user__first_name="John",
        user__has_premium=False,
        user__password=password,
    )
    api_client.log_in(km_user.user.primary_email.email, password)

    # ...then he should receive a 403 response if he tries to list the
    # accessors granting access to his account.
    response = api_client.get(URL)

    assert response.status_code == status.HTTP_403_FORBIDDEN
