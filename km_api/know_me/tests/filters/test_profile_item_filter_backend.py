from unittest import mock

from django.http import Http404

import pytest

from know_me import filters, models


def test_filter_list_inaccessible_row(
        api_rf,
        profile_row_factory,
        user_factory):
    """
    If a user does not have access to the given row, the filter should
    raise an ``Http404`` exception.
    """
    row = profile_row_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': row.pk}

    backend = filters.ProfileItemFilterBackend()

    with pytest.raises(Http404):
        backend.filter_list_queryset(
            request,
            models.ProfileItem.objects.all(),
            view)


def test_filter_list_nonexistent_row(
        api_rf,
        user_factory):
    """
    If there is no row with the given primary key, the filter should
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


def test_filter_list_row_items(api_rf, profile_item_factory):
    """
    The filter should only return profile items that belong to the row
    with the given primary key.
    """
    item = profile_item_factory()
    profile_item_factory()

    row = item.row
    group = row.group
    profile = group.profile

    api_rf.user = profile.user
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': row.pk}

    backend = filters.ProfileItemFilterBackend()
    results = backend.filter_list_queryset(
        request,
        models.ProfileItem.objects.all(),
        view)

    expected = row.items.all()

    assert list(results) == list(expected)
