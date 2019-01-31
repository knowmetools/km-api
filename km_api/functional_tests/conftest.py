from urllib.parse import urljoin

import pytest
import requests


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
            url = urljoin(self.base_url, url)

        return super().request(method, url, **kwargs)


@pytest.fixture
def api_client(live_server):
    """
    Returns:
        An API client instance configured to interact with a live server
        for testing.
    """
    return APIClient(live_server.url)
