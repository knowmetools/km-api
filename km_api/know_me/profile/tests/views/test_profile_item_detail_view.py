from unittest import mock

from know_me.profile import models, serializers, views


@mock.patch('know_me.profile.views.DRYPermissions.has_permission')
def test_check_permissions(mock_dry_permissions):
    """
    The view should use DRYPermissions to check object permissions.
    """
    view = views.ProfileItemDetailView()

    view.check_permissions(None)

    assert mock_dry_permissions.call_count == 1


def test_get_queryset(profile_item_factory):
    """
    The view should operate on all profile items.
    """
    profile_item_factory()
    profile_item_factory()
    profile_item_factory()

    view = views.ProfileItemDetailView()

    assert list(view.get_queryset()) == list(models.ProfileItem.objects.all())


def test_get_serializer_class():
    """
    Test the serializer class the view uses.
    """
    view = views.ProfileItemDetailView()
    expected = serializers.ProfileItemSerializer

    assert view.get_serializer_class() == expected
