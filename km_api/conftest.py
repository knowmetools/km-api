"""Pytest fixtures for the entire project.
"""

import io

from django.contrib.auth.models import AnonymousUser
from django.core.files.base import ContentFile

import PIL

import pytest

from rest_framework.test import APIRequestFactory

from account.factories import EmailFactory
import factories


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


@pytest.fixture(scope='function')
def api_rf():
    """
    Fixture to get a factory for making API requests.

    This fixture is scoped to functions so that we don't set a user on
    a factory instance and then reuse that user in a different test.

    Returns:
        A factory instance that can be used to make API requests. These
        requests can be made as a particular user by setting the
        ``user`` attribute of the factory instance.
    """
    return UserAPIRequestFactory(user=AnonymousUser())


@pytest.fixture
def email_factory(db):
    """
    Get the factory used to create email addresses.

    Returns:
        The factory class used to create ``EmailAddress`` instances.
    """
    return EmailFactory


@pytest.fixture
def image():
    """
    Fixture to get an image suitable for an ``ImageField``.

    Returns:
        A ``ContentFile`` containing a simple image.
    """
    image = PIL.Image.new('RGB', (200, 200), 'red')

    out_stream = io.BytesIO()
    image.save(out_stream, format='JPEG')

    return ContentFile(
        content=out_stream.getvalue(),
        name='foo.jpg')


@pytest.fixture
def serializer_context(api_rf):
    """
    Fixture to get context for serializer instantiation.

    Returns:
        dict:
            A dictionary containing dummy context for serializers.
    """
    return {
        'request': api_rf.get('/'),
    }


@pytest.fixture
def user_factory(db):
    """
    Fixture to get the factory used to create test users.

    Returns:
        The factory class used to create ``User`` instances.
    """
    return factories.UserFactory
