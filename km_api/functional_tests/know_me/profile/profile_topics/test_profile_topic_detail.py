from rest_framework import status

from test_utils import serialized_time


def test_delete_profile_topic(
    api_client, enable_premium_requirement, profile_topic_factory, user_factory
):
    """
    Premium users should be able to delete their own profile topics.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    topic = profile_topic_factory(profile__km_user__user=user)

    url = f"/know-me/profile/profile-topics/{topic.pk}/"
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_get_profile_topic(
    api_client, enable_premium_requirement, profile_topic_factory, user_factory
):
    """
    Premium users should be able to fetch their own profile topics.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    topic = profile_topic_factory(profile__km_user__user=user)

    url = f"/know-me/profile/profile-topics/{topic.pk}/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": topic.pk,
        "url": api_client.build_full_url(url),
        "created_at": serialized_time(topic.created_at),
        "updated_at": serialized_time(topic.updated_at),
        "is_detailed": topic.is_detailed,
        "items_url": api_client.build_full_url(f"{url}items/"),
        "name": topic.name,
        "permissions": {"read": True, "write": True},
        "profile_id": topic.profile.pk,
    }


def test_patch_profile_topic(
    api_client, enable_premium_requirement, profile_topic_factory, user_factory
):
    """
    Premium users should be able to update their own profile items.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    topic = profile_topic_factory(
        name="Old Topic", profile__km_user__user=user
    )

    url = f"/know-me/profile/profile-topics/{topic.pk}/"
    data = {"name": "New Name"}
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == data["name"]
