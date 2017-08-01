from rest_framework import status

from know_me import serializers, views


profile_topic_detail_view = views.ProfileTopicDetailView.as_view()


def test_get_own_topic(api_rf, profile_topic_factory):
    """
    Users should be able to access topics that are part of their own
    km_user.
    """
    topic = profile_topic_factory()
    group = topic.group
    km_user = group.km_user

    api_rf.user = km_user.user

    request = api_rf.get(topic.get_absolute_url())
    response = profile_topic_detail_view(request, pk=topic.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ProfileTopicSerializer(
        topic,
        context={'request': request})

    assert response.data == serializer.data


def test_update(api_rf, profile_topic_factory):
    """
    Sending a PATCH request to the view with valid data should update
    the given topic.
    """
    topic = profile_topic_factory(name='Old Name')
    group = topic.group
    km_user = group.km_user

    api_rf.user = km_user.user

    data = {
        'name': 'New Name',
    }

    request = api_rf.patch(topic.get_absolute_url(), data)
    response = profile_topic_detail_view(request, pk=topic.pk)

    assert response.status_code == status.HTTP_200_OK

    topic.refresh_from_db()
    serializer = serializers.ProfileTopicSerializer(
        topic,
        context={'request': request})

    assert response.data == serializer.data
