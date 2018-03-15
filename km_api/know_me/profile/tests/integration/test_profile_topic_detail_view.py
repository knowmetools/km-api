import pytest

from rest_framework import status

from know_me.profile import models, serializers


@pytest.mark.integration
def test_delete_profile_topic(api_client, profile_topic_factory):
    """
    Sending a DELETE request to the view should delete the profile topic
    with the specified ID.
    """
    topic = profile_topic_factory()
    api_client.force_authenticate(user=topic.profile.km_user.user)

    url = topic.get_absolute_url()
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert models.ProfileTopic.objects.count() == 0


@pytest.mark.integration
def test_get_profile_topic(api_client, api_rf, profile_topic_factory):
    """
    Sending a GET request to the view should return the specified
    profile topic's information.
    """
    topic = profile_topic_factory()
    user = topic.profile.km_user.user

    api_client.force_authenticate(user=user)
    api_rf.user = user

    url = topic.get_absolute_url()
    request = api_rf.get(url)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ProfileTopicListSerializer(
        topic,
        context={'request': request})

    assert response.data == serializer.data


@pytest.mark.integration
def test_update_profile_topic(api_client, profile_topic_factory):
    """
    Sending a PATCH request to the view should update the specified
    profile topic with the provided data.
    """
    topic = profile_topic_factory(name='Old Name')
    api_client.force_authenticate(user=topic.profile.km_user.user)

    data = {
        'name': 'New Name',
    }

    url = topic.get_absolute_url()
    response = api_client.patch(url, data)

    topic.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert topic.name == data['name']
