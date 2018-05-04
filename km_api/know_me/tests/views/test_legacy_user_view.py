from unittest import mock

from rest_framework import pagination

from know_me import models, serializers, views


@mock.patch(
    'know_me.views.DRYPermissions.has_permission',
    autospec=True)
def test_check_permissions(mock_dry_permissions):
    """
    The view should check for model permissions.
    """
    view = views.LegacyUserListView()

    view.check_permissions(None)

    assert mock_dry_permissions.call_count == 1


def test_get_queryset(legacy_user_factory):
    """
    The view should operate on all legacy users.
    """
    legacy_user_factory()
    legacy_user_factory()
    legacy_user_factory()

    view = views.LegacyUserListView()

    assert list(view.get_queryset()) == list(models.LegacyUser.objects.all())


def test_get_serializer_class():
    """
    Test the serializer class used for the view.
    """
    view = views.LegacyUserListView()

    assert view.get_serializer_class() == serializers.LegacyUserSerializer


def test_paginator():
    """
    The view should use a page number pagination style.
    """
    view = views.LegacyUserListView()

    assert isinstance(view.paginator, pagination.PageNumberPagination)
