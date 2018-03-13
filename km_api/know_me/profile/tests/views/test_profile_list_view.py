from unittest import mock

from know_me.profile import models, serializers, views


@mock.patch(
    'know_me.profile.views.DRYPermissions.has_permission',
    autospec=True)
@mock.patch(
    'know_me.profile.views.HasKMUserAccess.has_permission',
    autospec=True)
def test_check_permissions(mock_km_user_permission, mock_dry_permissions):
    """
    The view should check for model permissions as well as if the
    requesting user has access to the parent Know Me user.
    """
    view = views.ProfileListView()

    view.check_permissions(None)

    assert mock_km_user_permission.call_count == 1
    assert mock_dry_permissions.call_count == 1


@mock.patch('know_me.profile.views.KMUserAccessFilterBackend.filter_queryset')
@mock.patch(
    'know_me.profile.views.filters.ProfileFilterBackend.filter_queryset')
def test_filter_queryset(mock_profile_filter, mock_access_filter):
    """
    The view should filter its queryset by passing it through the filter
    that restricts access to items based on the owner.
    """
    view = views.ProfileListView()
    view.request = None

    queryset = models.Profile.objects.none()

    view.filter_queryset(queryset)

    assert mock_access_filter.call_count == 1
    assert mock_profile_filter.call_count == 1


def test_get_queryset(profile_factory):
    """
    The view should operate on all profiles.
    """
    profile_factory()
    profile_factory()
    profile_factory()

    view = views.ProfileListView()
    expected = models.Profile.objects.all()

    assert list(view.get_queryset()) == list(expected)


def test_get_serializer_class():
    """
    Test getting the serializer class the view uses.
    """
    view = views.ProfileListView()

    assert view.get_serializer_class() == serializers.ProfileListSerializer


def test_perform_create(km_user_factory):
    """
    When creating a new profile, it should be attached to the user
    specified in the URL.
    """
    km_user = km_user_factory()
    view = views.ProfileListView()
    view.kwargs = {'pk': km_user.pk}

    serializer = mock.Mock(name='Mock ProfileListSerializer')

    result = view.perform_create(serializer)

    assert result == serializer.save.return_value
    assert serializer.save.call_count == 1
    assert serializer.save.call_args[1] == {'km_user': km_user}
