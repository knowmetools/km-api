from unittest import mock

from django.http import Http404

import pytest

from know_me import filters, models


def test_filter_list_by_km_user(
        api_rf,
        emergency_contact_factory,
        km_user_factory):
    """
    The filter backend should return emergency items owned by the Know
    Me user whose ID is given in the URL.
    """
    km_user = km_user_factory()
    emergency_contact_factory(km_user=km_user)

    emergency_contact_factory()

    api_rf.user = km_user.user
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': km_user.pk}

    backend = filters.EmergencyContactFilterBackend()
    result = backend.filter_list_queryset(
        request,
        models.EmergencyContact.objects.all(),
        view)

    expected = km_user.emergency_contacts.all()

    assert list(result) == list(expected)


def test_filter_list_non_existent_user(api_rf, emergency_contact_factory):
    """
    If there is no Know Me user with the provided primary key, an
    Http404 exception should be raised.
    """
    ec = emergency_contact_factory()
    km_user = ec.km_user

    api_rf.user = km_user.user
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': km_user.pk + 1}

    backend = filters.EmergencyContactFilterBackend()

    with pytest.raises(Http404):
        backend.filter_list_queryset(
            request,
            models.EmergencyContact.objects.all(),
            view)


def test_filter_list_inaccessible_user(
        api_rf,
        emergency_contact_factory,
        user_factory):
    """
    If the requesting user does not have access to the user who owns the
    items, an Http404 exception should be raised.
    """
    ec = emergency_contact_factory()
    km_user = ec.km_user

    api_rf.user = user_factory()
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': km_user.pk}

    backend = filters.EmergencyContactFilterBackend()

    with pytest.raises(Http404):
        backend.filter_list_queryset(
            request,
            models.EmergencyContact.objects.all(),
            view)


def test_filter_list_shared(
        api_rf,
        emergency_contact_factory,
        km_user_accessor_factory,
        user_factory):
    """
    Users who have been invited to a Know Me user's account should be
    able to view that user's emergency contacts.
    """
    ec = emergency_contact_factory()
    km_user = ec.km_user

    user = user_factory()
    km_user_accessor_factory(
        accepted=True,
        km_user=km_user,
        user_with_access=user)

    api_rf.user = user
    request = api_rf.get('/')

    view = mock.Mock(name='Mock View')
    view.kwargs = {'pk': km_user.pk}

    backend = filters.EmergencyContactFilterBackend()
    filtered = backend.filter_list_queryset(
        request,
        models.EmergencyContact.objects.all(),
        view)

    expected = km_user.emergency_contacts.all()

    assert list(filtered) == list(expected)
