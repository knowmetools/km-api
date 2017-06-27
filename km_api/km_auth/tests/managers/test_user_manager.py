import pytest

from km_auth import models


@pytest.mark.django_db
def test_create_superuser():
    """
    Creating a superuser should act the same as ``create_user``, but it
    should set the ``is_staff`` and ``is_superuser`` flags to ``True``.
    """
    user = models.User.objects.create_superuser(
        email='test@example.com',
        first_name='John',
        last_name='Doe',
        password='p455w0rd')

    assert user.is_staff
    assert user.is_superuser


@pytest.mark.django_db
def test_create_user():
    """
    Creating a user should set the correct attributes on the user and
    hash the user's password.
    """
    password = 'p455w0rd'
    user = models.User.objects.create_user(
        email='test@example.com',
        first_name='John',
        last_name='Doe',
        password=password)

    assert user.check_password(password)
