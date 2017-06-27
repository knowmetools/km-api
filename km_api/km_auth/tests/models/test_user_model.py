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
