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
    os.environ['ADMIN_EMAIL'] = 'admin@example.com'
    os.environ['ADMIN_PASSWORD'] = 'password'

    output = io.StringIO()
    call_command('createadmin', out=output)

    assert get_user_model().objects.count() == 1

    admin = get_user_model().objects.get()

    assert admin.email == os.environ['ADMIN_EMAIL']
    assert admin.check_password(os.environ['ADMIN_PASSWORD'])
    assert admin.first_name == 'Admin'
    assert admin.last_name == 'User'
    assert admin.is_staff
    assert admin.is_superuser
    assert admin.email_addresses.count() == 1

    email = admin.email_addresses.get()

    assert email.email == os.environ['ADMIN_EMAIL']
    assert email.primary
    assert email.verified
