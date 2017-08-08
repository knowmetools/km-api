from unittest import mock

import pytest

from account import models


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
