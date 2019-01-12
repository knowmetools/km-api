import io
import os

from django.contrib.auth import get_user_model
from django.core.management import call_command

import pytest


@pytest.mark.django_db
def test_create_admin():
    """
    Calling the command with the appropriate environment variables set
    should create a new admin user. It should also create a verified
    email address for the user.
    """
    os.environ["ADMIN_EMAIL"] = "admin@example.com"
    os.environ["ADMIN_PASSWORD"] = "password"

    output = io.StringIO()
    call_command("createadmin", stdout=output)

    assert get_user_model().objects.count() == 1

    admin = get_user_model().objects.get()

    assert admin.check_password(os.environ["ADMIN_PASSWORD"])
    assert admin.first_name == "Admin"
    assert admin.last_name == "User"
    assert admin.is_staff
    assert admin.is_superuser
    assert admin.email_addresses.count() == 1

    email = admin.email_addresses.get()

    assert email.email == os.environ["ADMIN_EMAIL"]
    assert email.is_primary
    assert email.is_verified


def test_create_admin_user_exists(email_factory, user_factory):
    """
    If the user already exists, their information should be updated.
    """
    user = user_factory(password="oldpassword")
    email = user.primary_email

    os.environ["ADMIN_EMAIL"] = email.email
    os.environ["ADMIN_PASSWORD"] = "newpassword"

    output = io.StringIO()
    call_command("createadmin", stdout=output)

    assert get_user_model().objects.count() == 1

    user.refresh_from_db()
    email.refresh_from_db()

    assert user.check_password(os.environ["ADMIN_PASSWORD"])
    assert user.is_staff
    assert user.is_superuser

    assert email.is_verified
