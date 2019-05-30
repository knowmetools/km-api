from rest_framework import status

from test_utils import serialized_time


def test_get_list_entry(
    api_client,
    enable_premium_requirement,
    profile_list_entry_factory,
    user_factory,
):
    """
    The owner of a list entry associated with a profile item should be
    able to view it if they have an active premium subscription.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    list_entry = profile_list_entry_factory(
        profile_item__topic__profile__km_user__user=user
    )

    url = f"/know-me/profile/list-entries/{list_entry.pk}/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": list_entry.pk,
        "url": api_client.build_full_url(url),
        "created_at": serialized_time(list_entry.created_at),
        "updated_at": serialized_time(list_entry.updated_at),
        "permissions": {"read": True, "write": True},
        "profile_item_id": list_entry.profile_item.pk,
        "text": list_entry.text,
    }
