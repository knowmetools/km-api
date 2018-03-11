"""
Tests for the KMUserAccessFilterBackend class.

Note that the use of the ``KMUserAccessor`` model is just an example. We
could use any model that has a ``km_user`` owner.
"""

from unittest import mock

from django.http import Http404

import pytest

from know_me import filters, models


def test_filter_list_by_km_user(
        api_rf,
        km_user_accessor_factory,
        km_user_factory):
    """
    The filter backend should include items owned by the requesting user
    if that user's ID is also given in the URL.
    """
    km_user = km_user_factory()

    km_user_accessor_factory(km_user=km_user)
    km_user_accessor_factory()

    api_rf.user = km_user.user
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': km_user.pk}

    backend = filters.KMUserAccessFilterBackend()
    result = backend.filter_queryset(
        request,
        models.KMUserAccessor.objects.all(),
        view)

    expected = km_user.km_user_accessors.all()

    assert list(result) == list(expected)


def test_filter_list_non_existent_user(api_rf, user_factory):
    """
    If there is no Know Me user with the provided primary key, an
    Http404 exception should be raised.
    """
    api_rf.user = user_factory()
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': 1}

    backend = filters.KMUserAccessFilterBackend()

    with pytest.raises(Http404):
        backend.filter_queryset(
            request,
            models.KMUserAccessor.objects.all(),
            view)


def test_filter_list_inaccessible_user(
        api_rf,
        km_user_factory,
        user_factory):
    """
    If the requesting user does not have access to the user who owns the
    items, an Http404 exception should be raised.
    """
    km_user = km_user_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': km_user.pk}

    backend = filters.KMUserAccessFilterBackend()

    with pytest.raises(Http404):
        backend.filter_queryset(
            request,
            models.KMUserAccessor.objects.all(),
            view)


def test_filter_list_shared(
        api_rf,
        km_user_accessor_factory,
        user_factory):
    """
    The filter should include items where the requesting user has been
    granted access to the specified Know Me user through an accessor.
    """
    contact = km_user_accessor_factory()
    km_user = contact.km_user

    user = user_factory()
    km_user_accessor_factory(
        is_accepted=True,
        km_user=km_user,
        user_with_access=user)

    api_rf.user = user
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': km_user.pk}

    backend = filters.KMUserAccessFilterBackend()
    filtered = backend.filter_queryset(
        request,
        models.KMUserAccessor.objects.all(),
        view)

    expected = km_user.km_user_accessors.all()

    assert list(filtered) == list(expected)


def test_filter_list_shared_not_accepted(
        api_rf,
        km_user_accessor_factory,
        user_factory):
    """
    If the accessor has not been accepted then access to the shared
    items should not be granted.
    """
    contact = km_user_accessor_factory()
    km_user = contact.km_user

    user = user_factory()
    km_user_accessor_factory(
        is_accepted=False,
        km_user=km_user,
        user_with_access=user)

    api_rf.user = user
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': km_user.pk}

    backend = filters.KMUserAccessFilterBackend()

    with pytest.raises(Http404):
        backend.filter_queryset(
            request,
            models.KMUserAccessor.objects.all(),
            view)
