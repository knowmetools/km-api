from unittest import mock

from know_me import models


def test_create(media_resource_factory, km_user_factory):
    """
    Test creating an emergency item.
    """
    models.EmergencyItem.objects.create(
            description='This is a description.',
            media_resource=media_resource_factory(),
            km_user=km_user_factory(),
            name='Emergency Item')


def test_has_object_read_permission_with_user_permission(
        api_rf,
        emergency_item_factory):
    """
    If the requesting user has read permissions on the ``KMUser``
    instance the item belongs to, they should have read permissions on
    the item.
    """
    item = emergency_item_factory()

    api_rf.user = item.km_user.user
    request = api_rf.get('/')

    with mock.patch.object(
            item.km_user,
            'has_object_read_permission',
            return_value=True) as mock_permissions:
        assert item.has_object_read_permission(request)

    assert mock_permissions.call_count == 1
    assert mock_permissions.call_args[0] == (request,)


def test_has_object_read_permission_without_user_permission(
        api_rf,
        emergency_item_factory):
    """
    If the requesting user does not have read permissions on the
    ``KMUser`` instance the item belongs to, they should not have read
    permissions on the item.
    """
    item = emergency_item_factory()

    api_rf.user = item.km_user.user
    request = api_rf.get('/')

    with mock.patch.object(
            item.km_user,
            'has_object_read_permission',
            return_value=False) as mock_permissions:
        assert not item.has_object_read_permission(request)

    assert mock_permissions.call_count == 1
    assert mock_permissions.call_args[0] == (request,)


def test_has_object_write_permission_with_user_permission(
        api_rf,
        emergency_item_factory):
    """
    If the requesting user has write permissions on the ``KMUser``
    instance the item belongs to, they should have write permissions on
    the item.
    """
    item = emergency_item_factory()

    api_rf.user = item.km_user.user
    request = api_rf.get('/')

    with mock.patch.object(
            item.km_user,
            'has_object_write_permission',
            return_value=True) as mock_permissions:
        assert item.has_object_write_permission(request)

    assert mock_permissions.call_count == 1
    assert mock_permissions.call_args[0] == (request,)


def test_has_object_write_permission_without_user_permission(
        api_rf,
        emergency_item_factory):
    """
    If the requesting user does not have write permissions on the
    ``KMUser`` instance the item belongs to, they should not have write
    permissions on the item.
    """
    item = emergency_item_factory()

    api_rf.user = item.km_user.user
    request = api_rf.get('/')

    with mock.patch.object(
            item.km_user,
            'has_object_write_permission',
            return_value=False) as mock_permissions:
        assert not item.has_object_write_permission(request)

    assert mock_permissions.call_count == 1
    assert mock_permissions.call_args[0] == (request,)


def test_string_conversion(emergency_item_factory):
    """
    Converting an emergency item to a string should return the
    emergency item's name.
    """
    item = emergency_item_factory()

    assert str(item) == item.name
