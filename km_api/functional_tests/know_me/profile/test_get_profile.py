from rest_framework import status

from test_utils import serialized_time


def test_get_profile(
    api_client, enable_premium_requirement, profile_factory, user_factory
):
    """
    Premium users should be able to view their own profile.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    profile = profile_factory(km_user__user=user)

    url = f"/know-me/profile/profiles/{profile.pk}/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": profile.pk,
        "url": api_client.build_full_url(url),
        "created_at": serialized_time(profile.created_at),
        "updated_at": serialized_time(profile.updated_at),
        "is_private": profile.is_private,
        "name": profile.name,
        "permissions": {"read": True, "write": True},
        "topics": [],
        "topics_url": api_client.build_full_url(f"{url}topics/"),
    }
