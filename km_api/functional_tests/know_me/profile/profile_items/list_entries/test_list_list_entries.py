from rest_framework import status

from test_utils import serialized_time


def test_list_list_entries(
    api_client,
    enable_premium_requirement,
    profile_list_entry_factory,
    user_factory,
):
    """
    Premium users should be able to list the list entries belonging to
    profile items in their profile.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    entry = profile_list_entry_factory(
        profile_item__topic__profile__km_user__user=user
    )

    url = (
        f"/know-me/profile/profile-items/{entry.profile_item.pk}/list-entries/"
    )
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": entry.pk,
            "url": api_client.build_full_url(
                f"/know-me/profile/list-entries/{entry.pk}/"
            ),
            "created_at": serialized_time(entry.created_at),
            "updated_at": serialized_time(entry.updated_at),
            "permissions": {"read": True, "write": True},
            "profile_item_id": entry.profile_item.pk,
            "text": entry.text,
        }
    ]
