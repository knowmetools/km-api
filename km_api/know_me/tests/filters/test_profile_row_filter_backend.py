from unittest import mock

from django.http import Http404

import pytest

from know_me import filters, models


def test_filter_list_group_rows(api_rf, profile_row_factory):
    """
    The filter should return the rows belonging to the group whose
    primary key is given in the view.
    """
    row = profile_row_factory()
    profile_row_factory()

    group = row.group
    profile = group.profile

    api_rf.user = profile.user
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {
        'group_pk': group.pk,
    }

    backend = filters.ProfileRowFilterBackend()
    results = backend.filter_list_queryset(
        request,
        models.ProfileRow.objects.all(),
        view)

    expected = group.rows.all()

    assert list(results) == list(expected)


def test_filter_list_inaccessible_group(
        api_rf,
        profile_group_factory,
        user_factory):
    """
    Attempting to access the rows of a group that a user doesn't have
    access to should raise an ``Http404`` exception.
    """
    group = profile_group_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {
        'group_pk': group.pk,
    }

    backend = filters.ProfileRowFilterBackend()

    with pytest.raises(Http404):
        backend.filter_list_queryset(
            request,
            models.ProfileRow.objects.all(),
            view)


def test_filter_list_non_existent_group(api_rf, user_factory):
    """
    If there is no group with the given primary key, the filter should
    raise an ``Http404`` exception.
    """
    api_rf.user = user_factory()
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {
        'group_pk': 1,
    }

    backend = filters.ProfileRowFilterBackend()

    with pytest.raises(Http404):
        backend.filter_list_queryset(
            request,
            models.ProfileRow.objects.all(),
            view)
