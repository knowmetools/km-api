from unittest import mock

import pytest

from account import models


@pytest.mark.django_db
def test_confirm_pending():
    """
    Confirming a pending user should update the user's information with
    the data provided.
    """
    user = models.User.create_pending('test@example.com')

    first_name = 'John'
    last_name = 'Doe'
    password = 'p455w0rd'

    user.confirm_pending(
        first_name=first_name,
        last_name=last_name,
        password=password)

    user.refresh_from_db()

    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.check_password(password)

    assert not user.is_pending


def test_confirm_pending_not_pending(user_factory):
    """
    If we attempt to confirm a user who is not pending, an error should
    be raised.
    """
    user = user_factory()

    with pytest.raises(AssertionError):
        user.confirm_pending(first_name='foo', last_name='bar', password='baz')


@pytest.mark.django_db
def test_create():
    """
    Test creating a new user.
    """
    models.User.objects.create(
        email='test@example.com',
        is_active=True,
        is_pending=False,
        is_staff=True,
        is_superuser=True,
        first_name='John',
        last_name='Doe')


@pytest.mark.django_db
def test_create_pending():
    """
    The ``create_pending`` class method should create a user where
    ``is_pending`` is set to ``True``.
    """
    email = 'test@example.com'
    user = models.User.create_pending(email=email)

    assert user.email == email
    assert not user.has_usable_password()
    assert user.is_pending


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


def test_send_password_changed_email(settings, user_factory):
    """
    This method should send an email to the user informing them that
    their password has been changed.
    """
    user = user_factory()

    expected_context = {
        'user': user,
    }

    with mock.patch(
            'account.models.templated_email.send_email',
            autospec=True) as mock_send_email:
        user.send_password_changed_email()

    assert mock_send_email.call_count == 1
    assert mock_send_email.call_args[1] == {
        'context': expected_context,
        'subject': 'Your Know Me Password was Changed',
        'template': 'account/email/password-changed',
        'to': user.email,
    }
