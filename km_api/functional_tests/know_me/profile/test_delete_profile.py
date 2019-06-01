from rest_framework import status


def test_delete_profile(
    api_client, enable_premium_requirement, profile_factory, user_factory
):
    """
    Premium users should be able to delete their own profiles.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    profile = profile_factory(km_user__user=user)

    url = f"/know-me/profile/profiles/{profile.pk}/"
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
