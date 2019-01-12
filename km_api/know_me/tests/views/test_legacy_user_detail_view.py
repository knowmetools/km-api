from unittest import mock

from know_me import models, serializers, views


@mock.patch(
    "know_me.views.DRYGlobalPermissions.has_object_permission", autospec=True
)
def test_check_object_permissions(mock_dry_permissions, api_rf):
    """
    The view should check the permissions on the model.
    """
    view = views.LegacyUserDetailView()

    view.check_object_permissions(None, None)

    assert mock_dry_permissions.call_count == 1


def test_get_queryset(legacy_user_factory):
    """
    The view should operate on all legacy users.
    """
    legacy_user_factory()
    legacy_user_factory()
    legacy_user_factory()

    view = views.LegacyUserDetailView()
    expected = models.LegacyUser.objects.all()

    assert list(view.get_queryset()) == list(expected)


def test_get_serializer_class():
    """
    The view should utilize the detail serializer for legacy users.
    """
    view = views.LegacyUserDetailView()
    expected = serializers.LegacyUserSerializer

    assert view.get_serializer_class() == expected
