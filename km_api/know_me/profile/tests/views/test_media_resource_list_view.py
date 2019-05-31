from unittest import mock

from dry_rest_permissions.generics import DRYPermissions

import test_utils
from know_me.permissions import HasKMUserAccess, CollectionOwnerHasPremium
from know_me.profile import models, serializers, views


def test_get_permissions():
    """
    Test the permissions used by the view.
    """
    view = views.MediaResourceListView()

    assert test_utils.uses_permission_class(view, DRYPermissions)
    assert test_utils.uses_permission_class(view, HasKMUserAccess)
    assert test_utils.uses_permission_class(view, CollectionOwnerHasPremium)


def test_get_queryset(api_rf, media_resource_factory):
    """
    Given no GET parameters, the view should act on all media resources.
    """
    media_resource_factory()
    media_resource_factory()
    media_resource_factory()

    view = views.MediaResourceListView()
    view.request = view.initialize_request(api_rf.get("/"))

    expected = models.MediaResource.objects.all()

    assert list(view.get_queryset()) == list(expected)


def test_get_serializer():
    """
    The serializer for the view should be
    MediaResourceCategorySerializer.
    """
    view = views.MediaResourceListView()
    expected = serializers.MediaResourceSerializer

    assert view.get_serializer_class() == expected


def test_get_subscription_owner(km_user_factory):
    """
    The subscription owner for a collection of media resources should be
    the owner of the Know Me user whose resources are being accessed.
    """
    km_user = km_user_factory()
    view = views.MediaResourceListView()
    view.kwargs = {"pk": km_user.pk}
    request = mock.Mock()

    assert view.get_subscription_owner(request) == km_user.user


@mock.patch(
    "know_me.profile.views.KMUserAccessFilterBackend.filter_queryset",
    autospec=True,
)
def test_filter_queryset(mock_filter):
    """
    The queryset returned by the view should be passed through a filter
    to restrict access.
    """
    view = views.MediaResourceListView()
    view.request = None

    queryset = models.MediaResource.objects.none()

    view.filter_queryset(queryset)

    assert mock_filter.call_count == 1


def test_perform_create(km_user_factory):
    """
    The view should pass the Know Me user specified in the URL to the
    serializer when creating a new category.
    """
    km_user = km_user_factory()
    serializer = mock.Mock(name="Mock MediaResourceSerializer")

    view = views.MediaResourceListView()
    view.kwargs = {"pk": km_user.pk}

    assert view.perform_create(serializer) == serializer.save.return_value

    assert serializer.save.call_count == 1
    assert serializer.save.call_args[1] == {"km_user": km_user}
