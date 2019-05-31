from rest_framework import status


def test_sort_list_entries(
    api_client,
    enable_premium_requirement,
    profile_list_entry_factory,
    user_factory,
):
    """
    Premium users should be able to sort list entries with respect to
    their parent profile item.
    """
    password = "password"
    user = user_factory(has_premium=True, password="password")
    api_client.log_in(user.primary_email.email, password)

    e1 = profile_list_entry_factory(
        profile_item__topic__profile__km_user__user=user
    )
    e2 = profile_list_entry_factory(profile_item=e1.profile_item)

    data = {"order": [e2.pk, e1.pk]}
    url = f"/know-me/profile/profile-items/{e1.profile_item.pk}/list-entries/"
    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_200_OK

    sorted1, sorted2 = api_client.get(url).json()

    assert [sorted1["id"], sorted2["id"]] == data["order"]
