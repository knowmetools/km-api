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

    serializer = serializers.ProfileItemDetailSerializer(
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

    serializer = serializers.ProfileItemListSerializer(
        topic.items.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data


@pytest.mark.integration
def test_put_profile_order(
        api_client,
        api_rf,
        profile_item_factory,
        profile_topic_factory):
    """
    Sending a PUT request to the view should set the order of the
    profile topic's items.
    """
    topic = profile_topic_factory()
    user = topic.profile.km_user.user

    api_client.force_authenticate(user=user)
    api_rf.user = user

    i1 = profile_item_factory(topic=topic)
    i2 = profile_item_factory(topic=topic)
    i3 = profile_item_factory(topic=topic)

    data = {
        'order': [i1.id, i3.id, i2.id],
    }

    url = topic.get_item_list_url()
    request = api_rf.put(url, data)
    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ProfileItemListSerializer(
        topic.items.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data
    assert list(topic.get_profileitem_order()) == data['order']
