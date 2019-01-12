from unittest import mock

from know_me.profile import models, serializers, views


@mock.patch(
    "know_me.profile.views.DRYPermissions.has_permission", autospec=True
)
@mock.patch(
    "know_me.profile.views.HasKMUserAccess.has_permission", autospec=True
)
def test_check_permissions(mock_km_user_permission, mock_dry_permissions):
    """
    The view should check for model permissions as well as if the
    requesting user has access to the parent Know Me user.
    """
    view = views.MediaResourceListView()

    view.check_permissions(None)

    assert mock_km_user_permission.call_count == 1
    assert mock_dry_permissions.call_count == 1


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


def test_get_queryset_filtered(
    api_rf,
    km_user_factory,
    media_resource_category_factory,
    media_resource_factory,
):
    """
    If a category is specified, only the resources in that category
    should be returned.
    """
    km_user = km_user_factory()
    category = media_resource_category_factory(km_user=km_user)
    resource = media_resource_factory(category=category, km_user=km_user)

    media_resource_factory(km_user=km_user)

    view = views.MediaResourceListView()
    view.request = view.initialize_request(
        api_rf.get("/", {"category": category.pk})
    )

    assert list(view.get_queryset()) == [resource]


def test_get_serializer():
    """
    The serializer for the view should be
    MediaResourceCategorySerializer.
    """
    view = views.MediaResourceListView()
    expected = serializers.MediaResourceSerializer

    assert view.get_serializer_class() == expected


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
