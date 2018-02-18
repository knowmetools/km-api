import pytest

from rest_framework import status

from know_me.profile import serializers


@pytest.mark.integration
def test_create_profile_item(api_client, api_rf, profile_topic_factory):
    """
    Sending a POST request to the view should create a new item in the
    specified topic.
    """
    topic = profile_topic_factory()
    user = topic.profile.km_user.user

    api_client.force_authenticate(user=user)
    api_rf.user = user

    data = {
        'name': 'Test Item',
    }

    url = topic.get_item_list_url()
    request = api_rf.post(url, data)
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = serializers.ProfileItemSerializer(
        topic.items.get(),
        context={'request': request})

    assert response.data == serializer.data


@pytest.mark.integration
def test_get_profile_item_list(
        api_client,
        api_rf,
        profile_item_factory,
        profile_topic_factory):
    """
    Sending a GET request to the view should list the items that belong
    to the specified topic.
    """
    topic = profile_topic_factory()
    profile_item_factory(topic=topic)
    profile_item_factory(topic=topic)
    profile_item_factory()

    user = topic.profile.km_user.user
    api_client.force_authenticate(user=user)
    api_rf.user = user

    url = topic.get_item_list_url()
    request = api_rf.get(url)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ProfileItemSerializer(
        topic.items.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data
