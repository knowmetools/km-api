"""Pytest fixtures for the entire project.
"""

import io
import logging
import socket
import time
from threading import Thread

import pytest
from PIL import Image
from django.contrib.auth.models import AnonymousUser
from django.core.files.base import ContentFile
from rest_framework.test import APIClient, APIRequestFactory

import factories
import test_utils
from know_me.factories import SubscriptionAppleDataFactory
from test_utils.apple_receipt_validator import (
    apple_validator_app,
    AppleReceiptValidationClient,
)

logger = logging.getLogger(__name__)


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(("localhost", 0))
    address, port = s.getsockname()
    s.close()
    return port


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
def api_client():
    """
    Fixture to get a client for making API requests.

    Returns:
        An instance of the ``APIClient`` provided by DRF.
    """
    return APIClient()


@pytest.fixture(scope="function")
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
def apple_receipt_client(apple_validation_server, settings):
    host, port = apple_validation_server
    client = AppleReceiptValidationClient(
        f"http://{host}:{port}", settings.APPLE_SHARED_SECRET
    )

    yield client

    # After the client has been used, all enqueued mock responses should
    # be consumed.
    status = client.get_server_status()

    assert status["is_empty"], (
        "The Apple receipt validation server has queued status responses that "
        "were not consumed:\n{}"
    ).format(status["store"])


@pytest.fixture(autouse=True)
def apple_receipt_validation_settings(apple_validation_server, settings):
    host, port = apple_validation_server

    settings.APPLE_SHARED_SECRET = "mock-secret"
    settings.APPLE_RECEIPT_VALIDATION_ENDPOINT = f"http://{host}:{port}"


@pytest.fixture
def apple_subscription_factory(db):
    """
    Fixture to get the factory used to create Apple subscription data.
    """
    return SubscriptionAppleDataFactory


@pytest.fixture(autouse=True, scope="session")
def apple_validation_server():
    """
    Fixture to launch a server that mocks the implementation of the
    Apple receipt validation service.

    Returns:
        A tuple containing the hostname and port of the launched server.
    """
    port = get_free_port()
    mock_server_thread = Thread(
        target=apple_validator_app.run,
        kwargs={"host": "localhost", "port": port},
    )
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()

    # Give the Flask app time to boot
    logger.info("Booting mock Apple receipt validation server...")
    time.sleep(1)
    logger.info("Finished booting Apple receipt validation server.")

    return "localhost", port


@pytest.fixture
def email_confirmation_factory(db):
    """
    Fixture to get the factory used to create email confirmations.

    Returns:
        The factory used to create ``EmailConfirmation`` instances.
    """
    return factories.EmailConfirmationFactory


@pytest.fixture
def email_factory(db):
    """
    Get the factory used to create email addresses.

    Returns:
        The factory class used to create ``EmailAddress`` instances.
    """
    return factories.EmailFactory


@pytest.fixture
def image():
    """
    Fixture to get an image suitable for an ``ImageField``.

    Returns:
        A ``ContentFile`` containing a simple image.
    """
    image = Image.new("RGB", (200, 200), "red")

    out_stream = io.BytesIO()
    image.save(out_stream, format="png")

    return ContentFile(content=out_stream.getvalue(), name="foo.png")


@pytest.fixture(scope="session")
def serialized_time():
    """
    Fixture to get a function that returns a serialized version of a
    datetime instance.

    The output matches that of DRF's DateTimeField.
    """
    return test_utils.serialized_time


@pytest.fixture
def serializer_context(api_rf):
    """
    Fixture to get context for serializer instantiation.

    Returns:
        dict:
            A dictionary containing dummy context for serializers.
    """
    return {"request": api_rf.get("/")}


@pytest.fixture
def user_factory(db):
    """
    Fixture to get the factory used to create test users.

    Returns:
        The factory class used to create ``User`` instances.
    """
    return factories.UserFactory
