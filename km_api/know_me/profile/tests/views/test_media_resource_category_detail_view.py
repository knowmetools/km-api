from unittest import mock

from know_me.profile import models, serializers, views


@mock.patch(
    'know_me.profile.views.DRYPermissions.has_object_permission',
    autospec=True)
def test_check_object_permissions(mock_dry_permissions, api_rf):
    """
    The view should check the permissions on the model.
    """
    view = views.MediaResourceCategoryDetailView()

    view.check_object_permissions(None, None)

    assert mock_dry_permissions.call_count == 1


def test_get_queryset(media_resource_category_factory):
    """
    The view should operate on all media resource categories.
    """
    media_resource_category_factory()
    media_resource_category_factory()
    media_resource_category_factory()

    view = views.MediaResourceCategoryDetailView()
    expected = models.MediaResourceCategory.objects.all()

    assert list(view.get_queryset()) == list(expected)


def test_get_serializer_class():
    """
    The view should use MediaResourceCategorySerializer as its
    serializer class.
    """
    view = views.MediaResourceCategoryDetailView()
    expected = serializers.MediaResourceCategorySerializer

    assert view.get_serializer_class() == expected
