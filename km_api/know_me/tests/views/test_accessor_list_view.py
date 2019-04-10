from unittest import mock

import pytest
from django.http import Http404

from know_me import serializers, views


def test_get_queryset(api_rf, km_user_accessor_factory, km_user_factory):
    """
    The queryset for the view should include all accessors granting
    access to the requesting user's Know Me user.
    """
    km_user = km_user_factory()
    api_rf.user = km_user.user

    km_user_accessor_factory(km_user=km_user)
    km_user_accessor_factory(km_user=km_user)

    view = views.AccessorListView()
    view.request = api_rf.get("/")

    assert list(view.get_queryset()) == list(km_user.km_user_accessors.all())


def test_get_queryset_no_km_user(api_rf, user_factory):
    """
    If the requesting user has no associated Know Me user, a 404 error
    should be raised.
    """
    user = user_factory()
    api_rf.user = user

    view = views.AccessorListView()
    view.request = api_rf.get("/")

    with pytest.raises(Http404):
        view.get_queryset()


def test_get_serializer_class():
    """
    Test the serializer class used by the view.
    """
    view = views.AccessorListView()

    assert view.get_serializer_class() == serializers.KMUserAccessorSerializer


def test_perform_create(api_rf, km_user_factory):
    """
    If the requesting user has an associated Know Me user, that Know Me
    user should be passed to the serializer being saved.
    """
    km_user = km_user_factory()
    api_rf.user = km_user.user

    serializer = mock.Mock(name="Mock Serializer")
    view = views.AccessorListView()
    view.request = api_rf.post("/")

    view.perform_create(serializer)

    assert serializer.save.call_args[1] == {"km_user": km_user}


def test_perform_create_no_km_user(api_rf, user_factory):
    """
    If the requesting user does not have an associated Know Me user, the
    method should throw a 404 exception.
    """
    user = user_factory()
    api_rf.user = user

    serializer = mock.Mock(name="Mock Serializer")
    view = views.AccessorListView()
    view.request = api_rf.post("/")

    with pytest.raises(Http404):
        view.perform_create(serializer)
