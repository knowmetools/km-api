from rest_framework import status


def test_create_list_entry(
    api_client, enable_premium_requirement, profile_item_factory, user_factory
):
    """
    A profile owner with a premium subscription should be able to create
    a list entry for a profile item.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    item = profile_item_factory(topic__profile__km_user__user=user)

    url = f"/know-me/profile/profile-items/{item.pk}/list-entries/"
    data = {"text": "abc 123"}
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["text"] == data["text"]
