from unittest import mock

from know_me.profile import models, serializers, views


@mock.patch(
    "know_me.profile.views.DRYPermissions.has_permission", autospec=True
)
def test_check_permissions(mock_dry_permissions):
    """
    The view should check for model permissions as well as if the
    requesting user has access to the parent Know Me user.
    """
    view = views.ProfileDetailView()

    view.check_permissions(None)

    assert mock_dry_permissions.call_count == 1


def test_get_queryset(profile_factory):
    """
    The view should operate on all profiles.
    """
    profile_factory()
    profile_factory()
    profile_factory()

    view = views.ProfileDetailView()
    expected = models.Profile.objects.all()

    assert list(view.get_queryset()) == list(expected)


def test_get_serializer_class():
    """
    Test the serializer class used by the view.
    """
    view = views.ProfileDetailView()

    assert view.get_serializer_class() == serializers.ProfileDetailSerializer
