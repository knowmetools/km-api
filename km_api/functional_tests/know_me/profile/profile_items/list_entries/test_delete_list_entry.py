from rest_framework import status


def test_delete_list_entry(
    api_client,
    enable_premium_requirement,
    profile_list_entry_factory,
    user_factory,
):
    """
    The owner of a list entry should be able to delete it if they have
    an active premium subscription.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    list_entry = profile_list_entry_factory(
        profile_item__topic__profile__km_user__user=user
    )

    url = f"/know-me/profile/list-entries/{list_entry.pk}/"
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
