from unittest import mock

from dry_rest_permissions.generics import DRYPermissions

import test_utils
from know_me.permissions import ObjectOwnerHasPremium
from know_me.profile import models, serializers, views


def test_get_permissions():
    """
    Test the permissions used by the view.
    """
    view = views.MediaResourceDetailView()

    assert test_utils.uses_permission_class(view, DRYPermissions)
    assert test_utils.uses_permission_class(view, ObjectOwnerHasPremium)


def test_get_queryset(media_resource_factory):
    """
    The view should operate on all media resources.
    """
    media_resource_factory()
    media_resource_factory()
    media_resource_factory()

    view = views.MediaResourceDetailView()
    expected = models.MediaResource.objects.all()

    assert list(view.get_queryset()) == list(expected)


def test_get_serializer_class():
    """
    The view should use MediaResourceSerializer as its
    serializer class.
    """
    view = views.MediaResourceDetailView()
    expected = serializers.MediaResourceSerializer

    assert view.get_serializer_class() == expected


def test_get_subscription_owner():
    """
    The subscription owner for a media resource should be the user who
    owns the Know Me user who owns the resource.
    """
    view = views.MediaResourceDetailView()
    request = mock.Mock(name="Mock Request")
    resource = mock.Mock(name="Mock Media Resource")

    expected = resource.km_user.user

    assert view.get_subscription_owner(request, resource) == expected
