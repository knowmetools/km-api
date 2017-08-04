from unittest import mock

from django.http import Http404

import pytest

from know_me import filters, models


def test_filter_list_content_entries(api_rf, list_entry_factory):
    """
    The filter should return the entries belonging to the item whose
    primary key is given in the view.
    """
    list_entry = list_entry_factory()
    list_entry_factory()

    content = list_entry.list_content
    item = content.profile_item
    topic = item.topic
    profile = topic.profile
    km_user = profile.km_user

    api_rf.user = km_user.user
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': content.pk}

    backend = filters.ListEntryFilterBackend()
    results = backend.filter_list_queryset(
        request,
        models.ListEntry.objects.all(),
        view)

    expected = content.entries.all()

    assert list(results) == list(expected)


def test_filter_list_inaccessible_list_content(
        api_rf,
        list_content_factory,
        user_factory):
    """
    If the topic does not have access to the list, the filter should
    raise an ``Http404`` exception.
    """
    content = list_content_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': content.pk}

    backend = filters.ListEntryFilterBackend()

    with pytest.raises(Http404):
        backend.filter_list_queryset(
            request,
            models.ListEntry.objects.all(),
            view)


def test_filter_list_nonexistent_list_content(api_rf, user_factory):
    """
    If there is no list entry with the given primary key, the filter
    should raise an ``Http404`` exception.
    """
    api_rf.user = user_factory()
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': 1}

    backend = filters.ListEntryFilterBackend()

    with pytest.raises(Http404):
        backend.filter_list_queryset(
            request,
            models.ListEntry.objects.all(),
            view)
