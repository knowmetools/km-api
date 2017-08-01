from rest_framework import status

from know_me import models, serializers, views


profile_topic_list_view = views.ProfileTopicListView.as_view()


def test_create_topic(api_rf, profile_factory):
    """
    Sending a POST request with valid data to the view should create a
    new topic.
    """
    profile = profile_factory()
    km_user = profile.km_user

    api_rf.user = km_user.user

    data = {
        'name': 'Test Topic',
        'topic_type': models.ProfileTopic.TEXT,
    }

    request = api_rf.post(profile.get_topic_list_url(), data)
    response = profile_topic_list_view(request, pk=profile.pk)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = serializers.ProfileTopicSerializer(
        profile.topics.get(),
        context={'request': request})

    assert response.data == serializer.data


def test_list_own_topics(api_rf, profile_topic_factory):
    """
    Users should be able to list the topics in their own km_user.
    """
    topic = profile_topic_factory()
    profile = topic.profile
    km_user = profile.km_user

    api_rf.user = km_user.user

    request = api_rf.get(profile.get_topic_list_url())
    response = profile_topic_list_view(request, pk=profile.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ProfileTopicSerializer(
        [topic],
        context={'request': request},
        many=True)

    assert response.data == serializer.data
