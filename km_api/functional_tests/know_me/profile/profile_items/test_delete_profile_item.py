from rest_framework import status


def test_delete_profile_item(
    api_client, enable_premium_requirement, profile_item_factory, user_factory
):
    """
    Premium users should be able to delete profile items that they own.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    item = profile_item_factory(topic__profile__km_user__user=user)

    url = f"/know-me/profile/profile-items/{item.pk}/"
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
