from rest_framework import status

from know_me import models, serializers, views


profile_topic_list_view = views.ProfileTopicListView.as_view()


def test_create_topic(api_rf, profile_group_factory):
    """
    Sending a POST request with valid data to the view should create a
    new topic.
    """
    group = profile_group_factory()
    profile = group.profile

    api_rf.user = profile.user

    data = {
        'name': 'Test Topic',
        'topic_type': models.ProfileTopic.TEXT,
    }

    request = api_rf.post(group.get_topic_list_url(), data)
    response = profile_topic_list_view(request, pk=group.pk)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = serializers.ProfileTopicSerializer(
        group.topics.get(),
        context={'request': request})

    assert response.data == serializer.data


def test_list_own_topics(api_rf, profile_topic_factory):
    """
    Users should be able to list the topics in their own profile.
    """
    topic = profile_topic_factory()
    group = topic.group
    profile = group.profile

    api_rf.user = profile.user

    request = api_rf.get(group.get_topic_list_url())
    response = profile_topic_list_view(request, pk=group.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ProfileTopicSerializer(
        [topic],
        context={'request': request},
        many=True)

    assert response.data == serializer.data
