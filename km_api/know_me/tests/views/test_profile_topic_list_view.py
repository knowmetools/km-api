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


def test_get_shared_topics(
        api_rf,
        km_user_accessor_factory,
        km_user_factory,
        profile_factory,
        profile_topic_factory,
        user_factory):
    """
    Users who were granted access to a profile through an accessor
    should be able to list its profile items.
    """
    user = user_factory()
    profile = profile_factory()
    km_user = profile.km_user
    km_user_accessor_factory(
        accepted=True,
        km_user=km_user,
        user_with_access=user)

    profile_topic_factory(profile=profile)
    profile_topic_factory(profile=profile)

    api_rf.user = user

    request = api_rf.get(profile.get_topic_list_url())
    response = profile_topic_list_view(request, pk=profile.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ProfileTopicSerializer(
        profile.topics.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data


def test_get_shared_topics_not_accepted(
        api_rf,
        km_user_accessor_factory,
        km_user_factory,
        profile_factory,
        profile_topic_factory,
        user_factory):
    """
    Users who were granted access to a profile through an accessor that
    has not been accepted should not be able to list its profile items.
    """
    user = user_factory()
    profile = profile_factory()
    km_user = profile.km_user
    km_user_accessor_factory(
        accepted=False,
        km_user=km_user,
        user_with_access=user)

    profile_topic_factory(profile=profile)
    profile_topic_factory(profile=profile)

    api_rf.user = user

    request = api_rf.get(profile.get_topic_list_url())
    response = profile_topic_list_view(request, pk=profile.pk)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_shared_topics_private_profile(
        api_rf,
        km_user_accessor_factory,
        profile_factory,
        profile_topic_factory,
        user_factory):
    """
    The view should return topics in private profiles if the user has
    private profile access.
    """
    profile = profile_factory(is_private=True)

    km_user = profile.km_user
    user = user_factory()

    km_user_accessor_factory(
        accepted=True,
        has_private_profile_access=True,
        km_user=km_user,
        user_with_access=user)

    profile_topic_factory(profile=profile)
    profile_topic_factory(profile=profile)

    api_rf.user = user

    request = api_rf.get(profile.get_topic_list_url())
    response = profile_topic_list_view(request, pk=profile.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ProfileTopicSerializer(
        profile.topics.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data


def test_get_shared_topics_private_profile_no_access(
        api_rf,
        km_user_accessor_factory,
        profile_factory,
        profile_topic_factory,
        user_factory):
    """
    The view should not return topics in private profiles if the user
    has no private profile access.
    """
    profile = profile_factory(is_private=True)

    km_user = profile.km_user
    user = user_factory()

    km_user_accessor_factory(
        accepted=True,
        has_private_profile_access=False,
        km_user=km_user,
        user_with_access=user)

    profile_topic_factory(profile=profile)
    profile_topic_factory(profile=profile)

    api_rf.user = user

    request = api_rf.get(profile.get_topic_list_url())
    response = profile_topic_list_view(request, pk=profile.pk)

    assert response.status_code == status.HTTP_404_NOT_FOUND
