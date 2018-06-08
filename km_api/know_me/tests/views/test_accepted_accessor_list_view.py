from unittest import mock

from know_me import serializers, views


@mock.patch(
    'know_me.views.DRYPermissions.has_permission',
    autospec=True)
def test_check_permissions(mock_dry_permissions):
    """
    The view should check for model permissions.
    """
    view = views.AcceptedAccessorListView()

    view.check_permissions(None)

    assert mock_dry_permissions.call_count == 1


def test_get_queryset(api_rf, km_user_accessor_factory, user_factory):
    """
    The view should operate on the accessors owned by the requesting user.
    """
    user = user_factory()
    api_rf.user = user

    km_user_accessor_factory(is_accepted=True)
    km_user_accessor_factory(is_accepted=True, user_with_access=user)
    km_user_accessor_factory(is_accepted=False, user_with_access=user)

    view = views.AcceptedAccessorListView()
    view.request = api_rf.get('/')

    expected = user.km_user_accessors.filter(is_accepted=True)

    assert list(view.get_queryset()) == list(expected)


def test_get_serializer_class():
    """
    Test getting the serializer class the view uses.
    """
    view = views.AcceptedAccessorListView()

    assert view.get_serializer_class() == serializers.KMUserAccessorSerializer
