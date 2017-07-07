from unittest import mock

from django.http import Http404

import pytest

from know_me import filters, models


def test_filter_list_by_profile(api_rf, profile_group_factory):
    """
    The groups should be filtered to only those belonging to the profile
    whose primary key is specified in the view.
    """
    group = profile_group_factory()
    profile_group_factory()

    profile = group.profile

    api_rf.user = profile.user
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': profile.pk}

    backend = filters.ProfileGroupFilterBackend()
    result = backend.filter_list_queryset(
        request,
        models.ProfileGroup.objects.all(),
        view)

    expected = profile.groups.all()

    assert list(result) == list(expected)


def test_filter_list_non_existent_profile(api_rf, profile_group_factory):
    """
    If there is no profile with the given primary key, the filter should
    raise an ``Http404`` exception.
    """
    group = profile_group_factory()
    profile = group.profile

    api_rf.user = profile.user
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': profile.pk + 1}

    backend = filters.ProfileGroupFilterBackend()

    with pytest.raises(Http404):
        backend.filter_list_queryset(
            request,
            models.ProfileGroup.objects.all(),
            view)


def test_filter_list_unowned_profile(
        api_rf,
        profile_group_factory,
        user_factory):
    """
    If a user tries to list the groups of a profile they don't have
    access to, an ``Http404`` exception should be raised.
    """
    group = profile_group_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': group.profile.pk}

    backend = filters.ProfileGroupFilterBackend()

    with pytest.raises(Http404):
        backend.filter_list_queryset(
            request,
            models.ProfileGroup.objects.all(),
            view)
