from unittest import mock

from django.core.exceptions import ValidationError

import pytest

from rest_framework.serializers import (
    ValidationError as SerializerValidationError,
)
from rest_framework.settings import api_settings

from account.serializers import UserInfoSerializer
from know_me import serializers


def test_create(km_user_factory):
    """
    Saving the serializer should use the Know Me user's ``share`` method
    to create a new accessor.
    """
    km_user = km_user_factory()
    data = {
        'email': 'test@example.com',
        'is_admin': True,
    }

    serializer = serializers.KMUserAccessorSerializer(data=data)
    assert serializer.is_valid()

    with mock.patch.object(km_user, 'share', autospec=True) as mock_share:
        serializer.save(km_user=km_user)

    assert mock_share.call_count == 1
    assert mock_share.call_args[0] == (data['email'],)
    assert mock_share.call_args[1] == {'is_admin': data['is_admin']}


def test_create_failed(km_user_factory):
    """
    If the share operation fails, the validation error from the model
    should be translated to a serializer error.
    """
    km_user = km_user_factory()
    data = {
        'email': 'test@example.com',
    }

    serializer = serializers.KMUserAccessorSerializer(data=data)
    assert serializer.is_valid()

    with mock.patch.object(
        km_user,
        'share',
        side_effect=ValidationError('foo'),
    ) as mock_share:
        with pytest.raises(SerializerValidationError) as ex_info:
            serializer.save(km_user=km_user)

    assert mock_share.call_count == 1
    assert ex_info.value.detail == {
        api_settings.NON_FIELD_ERRORS_KEY: 'foo',
    }


def test_serialize(
        api_rf,
        km_user_factory,
        km_user_accessor_factory,
        serialized_time,
        user_factory):
    """
    Test serializing a km_user_accessor.
    """
    km_user = km_user_factory()
    user = user_factory()
    accessor = km_user_accessor_factory(
        email=user.primary_email.email,
        km_user=km_user,
        user_with_access=user)

    api_rf.user = user
    request = api_rf.get(accessor.get_absolute_url())

    serializer = serializers.KMUserAccessorSerializer(
        accessor,
        context={'request': request})

    km_user_serializer = serializers.KMUserInfoSerializer(
        km_user,
        context={'request': request},
    )
    user_serializer = UserInfoSerializer(
        accessor.user_with_access,
        context={'request': request})

    url = request.build_absolute_uri()

    accept_request = api_rf.get(accessor.accept_url)
    accept_url = accept_request.build_absolute_uri()

    expected = {
        'id': accessor.id,
        'url': url,
        'created_at': serialized_time(accessor.created_at),
        'updated_at': serialized_time(accessor.updated_at),
        'accept_url': accept_url,
        'email': accessor.email,
        'is_accepted': accessor.is_accepted,
        'is_admin': accessor.is_admin,
        'km_user': km_user_serializer.data,
        'permissions': {
            'accept': accessor.has_object_accept_permission(request),
            'destroy': accessor.has_object_destroy_permission(request),
            'read': accessor.has_object_read_permission(request),
            'write': accessor.has_object_write_permission(request),
        },
        'user_with_access': user_serializer.data,
    }

    assert serializer.data == expected


def test_validate_email_modified(km_user_accessor_factory):
    """
    Trying to set a new email on an existing accessor should cause the
    serializer to be invalid.
    """
    accessor = km_user_accessor_factory(email='old@example.com')
    data = {
        'email': 'new@example.com',
    }

    serializer = serializers.KMUserAccessorSerializer(accessor, data=data)

    assert not serializer.is_valid()
    assert set(serializer.errors.keys()) == {'email'}
