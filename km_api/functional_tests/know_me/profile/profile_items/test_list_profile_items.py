from rest_framework import status

from test_utils import serialized_time


def test_list_profile_items(
    api_client, enable_premium_requirement, profile_item_factory, user_factory
):
    """
    Premium users should be able to list their own profile items.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    item = profile_item_factory(topic__profile__km_user__user=user)

    url = f"/know-me/profile/profile-topics/{item.topic.pk}/items/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": item.pk,
            "url": api_client.build_full_url(
                f"/know-me/profile/profile-items/{item.pk}/"
            ),
            "created_at": serialized_time(item.created_at),
            "updated_at": serialized_time(item.updated_at),
            "description": item.description,
            "image": None,
            "list_entries_url": api_client.build_full_url(
                f"/know-me/profile/profile-items/{item.pk}/list-entries/"
            ),
            "name": item.name,
            "permissions": {"read": True, "write": True},
            "topic_id": item.topic.pk,
        }
    ]
