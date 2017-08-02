from unittest import mock

from django.http import Http404

import pytest

from know_me import filters, models


def test_filter_list_profile_topics(api_rf, profile_topic_factory):
    """
    The filter should return the topics belonging to the profile whose
    primary key is given in the view.
    """
    topic = profile_topic_factory()
    profile_topic_factory()

    profile = topic.profile
    km_user = profile.km_user

    api_rf.user = km_user.user
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': profile.pk}

    backend = filters.ProfileTopicFilterBackend()
    results = backend.filter_list_queryset(
        request,
        models.ProfileTopic.objects.all(),
        view)

    expected = profile.topics.all()

    assert list(results) == list(expected)


def test_filter_list_inaccessible_profile(
        api_rf,
        profile_factory,
        user_factory):
    """
    Attempting to access the topics of a profile that a user doesn't have
    access to should raise an ``Http404`` exception.
    """
    profile = profile_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': profile.pk}

    backend = filters.ProfileTopicFilterBackend()

    with pytest.raises(Http404):
        backend.filter_list_queryset(
            request,
            models.ProfileTopic.objects.all(),
            view)


def test_filter_list_non_existent_profile(api_rf, user_factory):
    """
    If there is no profile with the given primary key, the filter should
    raise an ``Http404`` exception.
    """
    api_rf.user = user_factory()
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': 1}

    backend = filters.ProfileTopicFilterBackend()

    with pytest.raises(Http404):
        backend.filter_list_queryset(
            request,
            models.ProfileTopic.objects.all(),
            view)
