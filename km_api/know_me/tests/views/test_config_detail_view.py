from unittest import mock

from know_me import serializers, views


@mock.patch("know_me.views.DRYGlobalPermissions.has_permission", autospec=True)
def test_check_permissions(mock_dry_permissions):
    """
    The view should check for model permissions.
    """
    view = views.ConfigDetailView()

    view.check_permissions(None)

    assert mock_dry_permissions.call_count == 1


@mock.patch("know_me.views.models.Config.get_solo", autospec=True)
@mock.patch(
    "know_me.views.ConfigDetailView.check_object_permissions", autospec=True
)
def test_get_object(mock_check_perms, mock_get, api_rf):
    """
    The view should use the method provided by django-solo to get or
    create the singleton. It should then check object permissions.
    """
    view = views.ConfigDetailView()
    view.request = api_rf.get("/")

    obj = view.get_object()

    assert mock_get.call_count == 1
    assert obj == mock_get.return_value

    assert mock_check_perms.call_count == 1
    assert mock_check_perms.call_args[0] == (view, view.request, obj)


def test_get_serializer_class():
    """
    Test the serializer class used by the view.
    """
    view = views.ConfigDetailView()

    assert view.get_serializer_class() == serializers.ConfigSerializer
