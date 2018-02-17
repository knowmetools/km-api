from unittest import mock

from know_me import models, serializers, views


@mock.patch(
    'know_me.views.DRYPermissions.has_permission',
    autospec=True)
@mock.patch(
    'know_me.views.permissions.HasKMUserAccess.has_permission',
    autospec=True)
def test_check_permissions(mock_km_user_permission, mock_dry_permissions):
    """
    The view should check for model permissions as well as if the
    requesting user has access to the parent Know Me user.
    """
    view = views.MediaResourceCategoryListView()

    view.check_permissions(None)

    assert mock_km_user_permission.call_count == 1
    assert mock_dry_permissions.call_count == 1


def test_get_queryset(media_resource_category_factory):
    """
    The view should act on all media resource categories.
    """
    media_resource_category_factory()
    media_resource_category_factory()
    media_resource_category_factory()

    view = views.MediaResourceCategoryListView()
    expected = models.MediaResourceCategory.objects.all()

    assert list(view.get_queryset()) == list(expected)


def test_get_serializer():
    """
    The serializer for the view should be
    MediaResourceCategorySerializer.
    """
    view = views.MediaResourceCategoryListView()
    expected = serializers.MediaResourceCategorySerializer

    assert view.get_serializer_class() == expected


@mock.patch(
    'know_me.views.filters.KMUserAccessFilterBackend.filter_queryset',
    autospec=True)
def test_filter_queryset(mock_filter):
    """
    The queryset returned by the view should be passed through a filter
    to restrict access.
    """
    view = views.MediaResourceCategoryListView()
    view.request = None

    queryset = models.MediaResourceCategory.objects.none()

    view.filter_queryset(queryset)

    assert mock_filter.call_count == 1


def test_perform_create(km_user_factory):
    """
    The view should pass the Know Me user specified in the URL to the
    serializer when creating a new category.
    """
    km_user = km_user_factory()
    serializer = mock.Mock(name='Mock MediaResourceCategorySerializer')

    view = views.MediaResourceCategoryListView()
    view.kwargs = {'pk': km_user.pk}

    assert view.perform_create(serializer) == serializer.save.return_value

    assert serializer.save.call_count == 1
    assert serializer.save.call_args[1] == {'km_user': km_user}
