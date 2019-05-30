from rest_framework import status


def test_update_list_entry(
    api_client,
    enable_premium_requirement,
    profile_list_entry_factory,
    user_factory,
):
    """
    The owner of a profile item list entry should be able to update it
    if they have an active premium subscription.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    list_entry = profile_list_entry_factory(
        profile_item__topic__profile__km_user__user=user, text="Old text"
    )

    url = f"/know-me/profile/list-entries/{list_entry.pk}/"
    data = {"text": "New text"}
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["text"] == data["text"]
