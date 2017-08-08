from unittest import mock

from django.http import Http404

import pytest

from know_me import filters, models


def test_filter_list_by_km_user(
        api_rf,
        emergency_item_factory,
        km_user_factory):
    """
    The filter backend should return emergency items owned by the Know
    Me user whose ID is given in the URL.
    """
    km_user = km_user_factory()
    emergency_item_factory(km_user=km_user)

    emergency_item_factory()

    api_rf.user = km_user.user
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': km_user.pk}

    backend = filters.EmergencyItemFilterBackend()
    result = backend.filter_list_queryset(
        request,
        models.EmergencyItem.objects.all(),
        view)

    expected = km_user.emergency_items.all()

    assert list(result) == list(expected)


def test_filter_list_non_existent_user(api_rf, emergency_item_factory):
    """
    If there is no Know Me user with the provided primary key, an
    Http404 exception should be raised.
    """
    item = emergency_item_factory()
    km_user = item.km_user

    api_rf.user = km_user.user
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': km_user.pk + 1}

    backend = filters.EmergencyItemFilterBackend()

    with pytest.raises(Http404):
        backend.filter_list_queryset(
            request,
            models.EmergencyItem.objects.all(),
            view)


def test_filter_list_inaccessible_user(
        api_rf,
        emergency_item_factory,
        user_factory):
    """
    If the requesting user does not have access to the user who owns the
    items, an Http404 exception should be raised.
    """
    item = emergency_item_factory()
    km_user = item.km_user

    api_rf.user = user_factory()
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': km_user.pk}

    backend = filters.EmergencyItemFilterBackend()

    with pytest.raises(Http404):
        backend.filter_list_queryset(
            request,
            models.EmergencyItem.objects.all(),
            view)
