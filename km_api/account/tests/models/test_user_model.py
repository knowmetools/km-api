import pytest

from account import models


@pytest.mark.django_db
def test_create():
    """
    Test creating a new user.
    """
    models.User.objects.create(
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
