from unittest import mock

from push_notifications.api.rest_framework import APNSDeviceSerializer

from notifications import views


@mock.patch(
    'notifications.views.IsAuthenticated.has_permission',
    autospec=True,
)
def test_check_permissions(mock_auth_perm):
    """
    The view should require an authenticated user.
    """
    view = views.APNSDeviceListView()
    view.check_permissions(None)

    assert mock_auth_perm.call_count == 1


def test_get_queryset(api_rf, apns_device_factory, user_factory):
    """
    The view should operate on the devices owned by the user specified
    in the view's keyword args.
    """
    user = user_factory()
    api_rf.user = user

    apns_device_factory(user=user)
    apns_device_factory()

    view = views.APNSDeviceListView()
    view.kwargs = {'pk': user.pk}
    view.request = api_rf.get('/')

    assert list(view.get_queryset()) == list(user.apnsdevice_set.all())


def test_get_serializer_class():
    """
    The view should use the APNS serializer provided by
    django-push-notifications.
    """
    view = views.APNSDeviceListView()

    assert view.get_serializer_class() == APNSDeviceSerializer


def test_perform_create(api_rf, user_factory):
    """
    When creating a new APNS device, the view should attach the
    requesting user to the device being created.
    """
    user = user_factory()
    api_rf.user = user

    view = views.APNSDeviceListView()
    view.request = api_rf.post('/')

    serializer = mock.Mock(name='Mock Serializer')

    view.perform_create(serializer)

    assert serializer.save.call_count == 1
    assert serializer.save.call_args[1] == {'user': user}
