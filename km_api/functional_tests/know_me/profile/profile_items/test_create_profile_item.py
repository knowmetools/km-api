from rest_framework import status


def test_create_profile_item(
    api_client, enable_premium_requirement, profile_topic_factory, user_factory
):
    """
    Premium users should be able to create profile items.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    topic = profile_topic_factory(profile__km_user__user=user)

    url = f"/know-me/profile/profile-topics/{topic.pk}/items/"
    data = {"name": "Test Item"}
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == data["name"]
