from django.core import mail
from django.template.loader import render_to_string

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


def test_send_password_changed_email(settings, user_factory):
    """
    This method should send an email to the user informing them that
    their password has been changed.
    """
    user = user_factory()
    expected_content = render_to_string(
        'account/email/password-changed.txt',
        {
            'user': user,
        })

    user.send_password_changed_email()

    assert len(mail.outbox) == 1

    email = mail.outbox[0]

    assert email.subject == 'Your Know Me Password was Changed'
    assert email.body == expected_content
    assert email.from_email == settings.DEFAULT_FROM_EMAIL
    assert email.to == [user.email]
