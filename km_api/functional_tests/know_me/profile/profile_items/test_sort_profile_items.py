from rest_framework import status


def test_sort_profile_items(
    api_client, enable_premium_requirement, profile_item_factory, user_factory
):
    """
    Premium users should be able to sort their profile items with
    respect to the parent topic.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    i1 = profile_item_factory(topic__profile__km_user__user=user)
    i2 = profile_item_factory(topic=i1.topic)

    url = f"/know-me/profile/profile-topics/{i1.topic.pk}/items/"
    data = {"order": [i2.pk, i1.pk]}
    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_200_OK

    # The collection should now be sorted
    items = api_client.get(url).json()

    assert list(map(lambda item: item["id"], items)) == data["order"]
