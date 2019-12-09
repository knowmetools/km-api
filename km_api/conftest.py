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
from know_me.factories import (
    AppleReceiptFactory,
    KMUserAccessorFactory,
    KMUserFactory,
    SubscriptionFactory,
)
from know_me.journal.factories import EntryCommentFactory, EntryFactory
from know_me.profile.factories import (
    ListEntryFactory,
    ProfileItemFactory,
    MediaResourceFactory,
    MediaResourceCoverStyleFactory,
    ProfileFactory,
    ProfileTopicFactory,
)
from test_utils.apple_receipt_validator import (
    AppleReceiptValidationClient,
    apple_validator_app,
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


@pytest.fixture
def apple_receipt_factory(db):
    """
    Returns:
        The factory class used to generate Apple receipts for testing.
    """
    return AppleReceiptFactory


@pytest.fixture(autouse=True)
def apple_receipt_validation_settings(apple_validation_server, settings):
    host, port = apple_validation_server

    settings.APPLE_SHARED_SECRET = "mock-secret"
    settings.APPLE_RECEIPT_VALIDATION_ENDPOINT = f"http://{host}:{port}"


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
def enable_premium_requirement(settings):
    """
    Fixture to enable the feature flag requiring certain operations to
    need a premium subscription.
    """
    settings.KNOW_ME_PREMIUM_ENABLED = True


@pytest.fixture
def entry_comment_factory(db):
    """
    Returns:
        The factory used to create journal entry comments for testing.
    """
    return EntryCommentFactory


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


@pytest.fixture
def journal_entry_comment_factory(db):
    """
    Fixture to get the factory used to create journal entry comments.
    """
    return EntryCommentFactory


@pytest.fixture
def journal_entry_factory(db):
    """
    Fixture to get the factory used to create journal entries.
    """
    return EntryFactory


@pytest.fixture
def km_user_accessor_factory(db):
    """
    Fixture to get the factory used to create km user accessors.

    Returns:
        The factory class used to create ``KMUser Access`` instances.
    """
    return KMUserAccessorFactory


@pytest.fixture
def km_user_factory(db):
    """
    Fixture to get the factory used to create a Know Me User.

    Returns:
        The factory class used to create test ``KMUser`` instances.
    """
    return KMUserFactory


@pytest.fixture
def media_resource_factory(db):
    """
    Fixture to get the factory used to create media resources.
    """
    return MediaResourceFactory


@pytest.fixture
def media_resource_cover_style_factory(db):
    """
    Fixture to get the factory used to create media resource cover styles.
    """
    return MediaResourceCoverStyleFactory


@pytest.fixture
def profile_factory(db):
    """
    Fixture to get the factory used to create profiles.
    """
    return ProfileFactory


@pytest.fixture
def profile_item_factory(db):
    """
    Fixture to get the factory used to create profile items.
    """
    return ProfileItemFactory


@pytest.fixture
def profile_list_entry_factory(db):
    """
    Fixture to get the factory used to create list entries for profile
    items.
    """
    return ListEntryFactory


@pytest.fixture
def profile_topic_factory(db):
    """
    Fixture to get the factory used to create profile topics.
    """
    return ProfileTopicFactory


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
def subscription_factory(db):
    """
    Fixture to get the factory used to create subscriptions.
    """
    return SubscriptionFactory


@pytest.fixture
def user_factory(db):
    """
    Fixture to get the factory used to create test users.

    Returns:
        The factory class used to create ``User`` instances.
    """
    return factories.UserFactory
