import pytest

from km_auth import models


@pytest.mark.django_db
def test_create():
    """
    Test creating a new user.
    """
    models.User.objects.create(
        email='test@example.com',
        is_active=True,
        is_staff=True,
        is_superuser=True,
        first_name='John',
        last_name='Doe')


def test_get_full_name(user_factory):
    """
    A user's full name should be composed of their first and last name.
    """
    user = user_factory()
    expected = '{first} {last}'.format(
        first=user.first_name,
        last=user.last_name)

    assert user.get_full_name() == expected


def test_get_short_name(user_factory):
    """
    A user's short name should be their first name.
    """
    user = user_factory()

    assert user.get_short_name() == user.first_name
