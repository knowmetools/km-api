from rest_framework import status

from test_utils import serialized_time


def test_get_profile_topics(
    api_client, enable_premium_requirement, profile_topic_factory, user_factory
):
    """
    Premium users should be able to list their own profile topics.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    topic = profile_topic_factory(profile__km_user__user=user)

    url = f"/know-me/profile/profiles/{topic.profile.pk}/topics/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": topic.pk,
            "url": api_client.build_full_url(
                f"/know-me/profile/profile-topics/{topic.pk}/"
            ),
            "created_at": serialized_time(topic.created_at),
            "updated_at": serialized_time(topic.updated_at),
            "is_detailed": topic.is_detailed,
            "items_url": api_client.build_full_url(
                f"/know-me/profile/profile-topics/{topic.pk}/items/"
            ),
            "name": topic.name,
            "permissions": {"read": True, "write": True},
            "profile_id": topic.profile.pk,
        }
    ]


def test_post_create_topic(
    api_client, enable_premium_requirement, profile_factory, user_factory
):
    """
    Premium users should be able to add new topics to their own
    profiles.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    profile = profile_factory(km_user__user=user)

    url = f"/know-me/profile/profiles/{profile.pk}/topics/"
    data = {"name": "Test Topic"}
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == data["name"]


def test_put_topic_order(
    api_client, enable_premium_requirement, profile_topic_factory, user_factory
):
    """
    Premium users should be able to sort their own profile topics with
    respect to the parent profile.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    t1 = profile_topic_factory(profile__km_user__user=user)
    t2 = profile_topic_factory(profile=t1.profile)

    url = f"/know-me/profile/profiles/{t1.profile.pk}/topics/"
    data = {"order": [t2.pk, t1.pk]}
    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_200_OK

    # The collection should now be sorted
    topics = api_client.get(url).json()

    assert list(map(lambda topic: topic["id"], topics)) == data["order"]
