from unittest import mock

from account import models, views, serializers


@mock.patch('account.views.permissions.IsStaff.has_permission')
def test_check_permissions(mock_has_permission):
    """
    The view should require a staff user.
    """
    view = views.UserListView()

    view.check_permissions(None)

    assert mock_has_permission.call_count == 1


def test_get_queryset(user_factory):
    """
    The view should operate on all users.
    """
    user_factory()
    user_factory()
    user_factory()

    view = views.UserListView()

    assert list(view.get_queryset()) == list(models.User.objects.all())


def test_get_serializer_class():
    """
    Test the serializer class used by the view.
    """
    view = views.UserListView()

    assert view.get_serializer_class() == serializers.UserListSerializer
