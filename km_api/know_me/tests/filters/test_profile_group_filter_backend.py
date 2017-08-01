from unittest import mock

from django.http import Http404

import pytest

from know_me import filters, models


def test_filter_list_by_km_user(api_rf, profile_group_factory):
    """
    The groups should be filtered to only those belonging to the km_user
    whose primary key is specified in the view.
    """
    group = profile_group_factory()
    profile_group_factory()

    km_user = group.km_user

    api_rf.user = km_user.user
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': km_user.pk}

    backend = filters.ProfileGroupFilterBackend()
    result = backend.filter_list_queryset(
        request,
        models.ProfileGroup.objects.all(),
        view)

    expected = km_user.groups.all()

    assert list(result) == list(expected)


def test_filter_list_non_existent_km_user(api_rf, profile_group_factory):
    """
    If there is no km_user with the given primary key, the filter should
    raise an ``Http404`` exception.
    """
    group = profile_group_factory()
    km_user = group.km_user

    api_rf.user = km_user.user
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': km_user.pk + 1}

    backend = filters.ProfileGroupFilterBackend()

    with pytest.raises(Http404):
        backend.filter_list_queryset(
            request,
            models.ProfileGroup.objects.all(),
            view)


def test_filter_list_unowned_km_user(
        api_rf,
        profile_group_factory,
        user_factory):
    """
    If a user tries to list the groups of a km_user they don't have
    access to, an ``Http404`` exception should be raised.
    """
    group = profile_group_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': group.km_user.pk}

    backend = filters.ProfileGroupFilterBackend()

    with pytest.raises(Http404):
        backend.filter_list_queryset(
            request,
            models.ProfileGroup.objects.all(),
            view)
