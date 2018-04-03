import pytest

from rest_framework import status

from know_me.profile import serializers


@pytest.mark.integration
def test_get_profile_topics(
        api_client,
        api_rf,
        profile_factory,
        profile_topic_factory):
    """
    Sending a GET request to the view should return a list of the topics
    in the specified profile.
    """
    profile = profile_factory()
    profile_topic_factory(profile=profile)
    profile_topic_factory(profile=profile)
    profile_topic_factory()

    api_client.force_authenticate(user=profile.km_user.user)
    api_rf.user = profile.km_user.user

    url = profile.get_topic_list_url()
    request = api_rf.get(url)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ProfileTopicListSerializer(
        profile.topics.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data


@pytest.mark.integration
def test_post_profile_topic(
        api_client,
        api_rf,
        profile_factory):
    """
    Sending a POST request to the view should create a new profile topic
    for the specified profile.
    """
    profile = profile_factory()

    api_client.force_authenticate(user=profile.km_user.user)
    api_rf.user = profile.km_user.user

    data = {
        'name': 'Test Topic',
    }

    url = profile.get_topic_list_url()
    request = api_rf.post(url, data)
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = serializers.ProfileTopicDetailSerializer(
        profile.topics.get(),
        context={'request': request})

    assert response.data == serializer.data


@pytest.mark.integration
def test_put_profile_order(
        api_client,
        api_rf,
        profile_factory,
        profile_topic_factory):
    """
    Sending a PUT request to the view should set the order of the
    profile's topics.
    """
    profile = profile_factory()

    api_client.force_authenticate(user=profile.km_user.user)
    api_rf.user = profile.km_user.user

    t1 = profile_topic_factory(profile=profile)
    t2 = profile_topic_factory(profile=profile)
    t3 = profile_topic_factory(profile=profile)

    data = {
        'order': [t1.id, t3.id, t2.id],
    }

    url = profile.get_topic_list_url()
    request = api_rf.put(url, data)
    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ProfileTopicListSerializer(
        profile.topics.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data
    assert list(profile.get_profiletopic_order()) == data['order']
