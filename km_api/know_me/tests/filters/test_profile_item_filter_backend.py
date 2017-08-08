from unittest import mock

from django.http import Http404

import pytest

from know_me import filters, models


def test_filter_list_inaccessible_topic(
        api_rf,
        profile_topic_factory,
        user_factory):
    """
    If a user does not have access to the given topic, the filter should
    raise an ``Http404`` exception.
    """
    topic = profile_topic_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': topic.pk}

    backend = filters.ProfileItemFilterBackend()

    with pytest.raises(Http404):
        backend.filter_list_queryset(
            request,
            models.ProfileItem.objects.all(),
            view)


def test_filter_list_nonexistent_topic(
        api_rf,
        user_factory):
    """
    If there is no topic with the given primary key, the filter should
    raise an ``Http404`` exception.
    """
    api_rf.user = user_factory()
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': 1}

    backend = filters.ProfileItemFilterBackend()

    with pytest.raises(Http404):
        backend.filter_list_queryset(
            request,
            models.ProfileItem.objects.all(),
            view)


def test_filter_list_topic_items(api_rf, profile_item_factory):
    """
    The filter should only return profile items that belong to the topic
    with the given primary key.
    """
    item = profile_item_factory()
    profile_item_factory()

    topic = item.topic
    profile = topic.profile
    km_user = profile.km_user

    api_rf.user = km_user.user
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': topic.pk}

    backend = filters.ProfileItemFilterBackend()
    results = backend.filter_list_queryset(
        request,
        models.ProfileItem.objects.all(),
        view)

    expected = topic.items.all()

    assert list(results) == list(expected)
