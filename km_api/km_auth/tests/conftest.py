"""Fixtures for pytest.
"""

from django.contrib.auth.models import AnonymousUser

import pytest

from rest_framework.test import APIRequestFactory

from km_auth import factories


class UserAPIRequestFactory(APIRequestFactory):
    """
    Request factory that makes all requests as a particular user.
    """

    def __init__(self, user, *args, **kwargs):
        """
        Create a new request factory.

        Args:
            user:
                The user to associate with all requests.
            args:
                Positional arguments to pass to the parent request
                factory.
            kwargs:
                Keyword arguments to pass to the parent request factory.
        """
        super().__init__(*args, **kwargs)

        self.user = user

    def generic(self, *args, **kwargs):
        """
        Make a generic request from the factory's user.

        Args:
            args:
                Positional arguments to pass to the super class'
                ``generic`` method.
            kwargs:
                Keyword arguments to pass to the super class'
                ``generic`` method.

        Returns:
            A new request associated with the factory's user.
        """
        request = super().generic(*args, **kwargs)
        request.user = self.user

        return request


@pytest.fixture
def admin_api_rf(user_factory):
    """
    Fixture to get a factory for making authenticated API requests.

    Returns:
        A factory that makes requests as an admin user.
    """
    user = user_factory(is_superuser=True)

    return UserAPIRequestFactory(user=user)


@pytest.fixture(scope='session')
def anon_api_rf():
    """
    Fixture to get a factory for making anonymous API requests.

    Returns:
        A factory that makes requests as an anonymous user.
    """
    user = AnonymousUser()

    return UserAPIRequestFactory(user=user)


@pytest.fixture(scope='session')
def api_rf():
    """
    Fixture to get a factory for making API requests.

    Returns:
        A factory that can be used to create API requests.
    """
    return APIRequestFactory()


@pytest.fixture
def user_factory(db):
    """
    Fixture to get the class used to create ``User`` instances.

    Returns:
        ``km_auth.factories.UserFactory``
    """
    return factories.UserFactory
