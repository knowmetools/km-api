from rest_framework import status


def test_sort_profiles(
    api_client, enable_premium_requirement, profile_factory, user_factory
):
    """
    Premium users should be able to sort their profiles.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    p1 = profile_factory(km_user__user=user)
    p2 = profile_factory(km_user=p1.km_user)

    url = f"/know-me/users/{user.km_user.pk}/profiles/"
    data = {"order": [p2.pk, p1.pk]}
    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_200_OK

    # The profile list should now be correctly ordered
    profiles = api_client.get(url).json()

    assert list(map(lambda profile: profile["id"], profiles)) == data["order"]
