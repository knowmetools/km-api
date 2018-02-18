from unittest import mock

from django.core.exceptions import ValidationError

import pytest

from know_me import models


def test_create(km_user_factory):
    """
    Test creating an emergency contact.
    """
    models.EmergencyContact.objects.create(
        km_user=km_user_factory(),
        name='First Last',
        relation='Parent',
        phone_number='19199199199',
        alt_phone_number='12345678909',
        email='hi@gmail.com')


def test_has_object_read_permission_with_user_permission(
        api_rf,
        emergency_contact_factory):
    """
    If the requesting user has read permissions on the ``KMUser``
    instance the contact belongs to, they should have read permissions on
    the contact.
    """
    ec = emergency_contact_factory()

    api_rf.user = ec.km_user.user
    request = api_rf.get('/')

    with mock.patch.object(
            ec.km_user,
            'has_object_read_permission',
            return_value=True) as mock_permissions:
        assert ec.has_object_read_permission(request)

    assert mock_permissions.call_count == 1
    assert mock_permissions.call_args[0] == (request,)


def test_has_object_read_permission_without_user_permission(
        api_rf,
        emergency_contact_factory):
    """
    If the requesting user does not have read permissions on the
    ``KMUser`` instance the contact belongs to, they should not have read
    permissions on the contact.
    """
    ec = emergency_contact_factory()

    api_rf.user = ec.km_user.user
    request = api_rf.get('/')

    with mock.patch.object(
            ec.km_user,
            'has_object_read_permission',
            return_value=False) as mock_permissions:
        assert not ec.has_object_read_permission(request)

    assert mock_permissions.call_count == 1
    assert mock_permissions.call_args[0] == (request,)


def test_has_object_write_permission_with_user_permission(
        api_rf,
        emergency_contact_factory):
    """
    If the requesting user has write permissions on the ``KMUser``
    instance the contact belongs to, they should have write permissions on
    the contact.
    """
    ec = emergency_contact_factory()

    api_rf.user = ec.km_user.user
    request = api_rf.get('/')

    with mock.patch.object(
            ec.km_user,
            'has_object_write_permission',
            return_value=True) as mock_permissions:
        assert ec.has_object_write_permission(request)

    assert mock_permissions.call_count == 1
    assert mock_permissions.call_args[0] == (request,)


def test_has_object_write_permission_without_user_permission(
        api_rf,
        emergency_contact_factory):
    """
    If the requesting user does not have write permissions on the
    ``KMUser`` instance the contact belongs to, they should not have write
    permissions on the contact.
    """
    ec = emergency_contact_factory()

    api_rf.user = ec.km_user.user
    request = api_rf.get('/')

    with mock.patch.object(
            ec.km_user,
            'has_object_write_permission',
            return_value=False) as mock_permissions:
        assert not ec.has_object_write_permission(request)

    assert mock_permissions.call_count == 1
    assert mock_permissions.call_args[0] == (request,)


def test_invalid_phone_number(emergency_contact_factory):
    """
    Test creating an emergency contact with invalid phone number
    """
    with pytest.raises(ValidationError):
        ec = emergency_contact_factory(phone_number='1234567890123456')
        ec.full_clean()


def test_invalid_alt_phone_number(emergency_contact_factory):
    """
    Test creating an emergency contact with invalid phone number
    """
    with pytest.raises(ValidationError):
        ec = emergency_contact_factory(alt_phone_number='12345')
        ec.full_clean()


def test_string_conversion(emergency_contact_factory):
    """
    Converting an emergency contact to a string should return the
    contact's name.
    """
    ec = emergency_contact_factory()

    assert str(ec) == ec.name
