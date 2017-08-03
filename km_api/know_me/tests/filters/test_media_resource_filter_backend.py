from unittest import mock

from django.http import Http404

import pytest

from know_me import filters, models


def test_filter_list_by_km_user(
        api_rf,
        km_user_factory,
        media_resource_factory):
    """
    The filter backend should return media resources owned by the Know
    Me user whose ID is given in the URL.
    """
    km_user = km_user_factory()
    media_resource_factory(km_user=km_user)

    media_resource_factory()

    api_rf.user = km_user.user
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': km_user.pk}

    backend = filters.MediaResourceFilterBackend()
    result = backend.filter_list_queryset(
        request,
        models.MediaResource.objects.all(),
        view)

    expected = km_user.media_resources.all()

    assert list(result) == list(expected)


def test_filter_list_non_existent_user(api_rf, media_resource_factory):
    """
    If there is no Know Me user with the provided primary key, an
    Http404 exception should be raised.
    """
    resource = media_resource_factory()
    km_user = resource.km_user

    api_rf.user = km_user.user
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': km_user.pk + 1}

    backend = filters.MediaResourceFilterBackend()

    with pytest.raises(Http404):
        backend.filter_list_queryset(
            request,
            models.MediaResource.objects.all(),
            view)


def test_filter_list_inaccessible_user(
        api_rf,
        media_resource_factory,
        user_factory):
    """
    If the requesting user does not have access to the user who owns the
    resources, an Http404 exception should be raised.
    """
    resource = media_resource_factory()
    km_user = resource.km_user

    api_rf.user = user_factory()
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': km_user.pk}

    backend = filters.MediaResourceFilterBackend()

    with pytest.raises(Http404):
        backend.filter_list_queryset(
            request,
            models.MediaResource.objects.all(),
            view)
