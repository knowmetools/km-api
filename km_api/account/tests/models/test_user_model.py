from unittest import mock

import pytest

from account import models


@pytest.mark.django_db
def test_create(image):
    """
    Test creating a new user.
    """
    models.User.objects.create(
        image=image,
        is_active=True,
        is_staff=True,
        is_superuser=True,
        first_name="John",
        last_name="Doe",
    )


def test_get_full_name(user_factory):
    """
    A user's full name should be composed of their first and last name.
    """
    user = user_factory()
    expected = "{first} {last}".format(
        first=user.first_name, last=user.last_name
    )

    assert user.get_full_name() == expected


def test_get_short_name(user_factory):
    """
    A user's short name should be their first name.
    """
    user = user_factory()

    assert user.get_short_name() == user.first_name


@mock.patch("account.models.uuid.uuid4")
def test_get_user_image_path(mock_uuid):
    """
    User images should be uploaded to the 'users/' directory using a
    UUID as the filename.
    """
    filename = "foo.jpg"

    result = models.get_user_image_path(None, "foo.jpg")
    expected = "users/{name}.{ext}".format(
        ext=filename.rsplit(".", 1)[-1], name=mock_uuid.return_value
    )

    assert mock_uuid.call_count == 1
    assert result == expected


def test_primary_email(email_factory, user_factory):
    """
    The 'primary_email' property should return the email address owned
    by the user that has 'is_primary' set to true.
    """
    user = user_factory()
    primary = email_factory(is_primary=True, user=user)
    primary.set_primary()

    email_factory(user=user)

    assert user.primary_email == primary


def test_primary_email_no_primary(user_factory):
    """
    If the user has no primary email address, None should be returned.
    """
    user = user_factory()
    user.email_addresses.update(is_primary=False)

    assert user.primary_email is None
