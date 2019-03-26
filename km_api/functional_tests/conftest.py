from urllib.parse import urljoin

import pytest
import requests
from rest_framework.reverse import reverse


class APIClient(requests.Session):
    """
    Client for interacting with the API.
    """

    def __init__(self, url):
        """
        Initialize the API client.

        Args:
            url:
                The base URL to make requests to.
        """
        super().__init__()

        self.base_url = url

    def build_full_url(self, path):
        """
        Build a full URL from an absolute path.

        Args:
            path:
                The absolute path to create a full URL for.

        Returns:
            The given path prepended with the base URL of the client.
        """
        return urljoin(self.base_url, path)

    def log_in(self, email, password):
        """
        Log in to the API and persist the returned token.

        Args:
            email:
                The email address of the user to log in as.
            password:
                The password of the user to log in as.
        """
        url = reverse("auth:login")
        response = self.post(url, json={"email": email, "password": password})
        response.raise_for_status()

        self.headers.update(
            {"Authorization": f'Token {response.json()["token"]}'}
        )

    def request(self, method, url, **kwargs):
        """
        Make a request.

        Args:
            method:
                The method to use to make the request.
            url:
                The URL to send the request to. If the URL does not
                begin with a protocol, it is appended to the client's
                base URL.
            **kwargs:
                Additional kwargs to pass to the underlying
                :class:`requests.Session`.

        Returns:
            The response returned from the server at the provided URL.
        """
        if not url.startswith("http"):
            url = self.build_full_url(url)

        return super().request(method, url, **kwargs)


@pytest.fixture
def api_client(live_server):
    """
    Returns:
        An API client instance configured to interact with a live server
        for testing.
    """
    return APIClient(live_server.url)
