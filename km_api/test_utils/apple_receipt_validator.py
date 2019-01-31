"""
A mock server for faking Apple receipt validation.

The root endpoint of the service acts as if it were the actual receipt
validation endpoint. Additional endpoints are used to manipulate the
returned data for testing purposes.
"""
from collections import defaultdict
from urllib.parse import urljoin

import requests
from flask import Flask, jsonify, request

apple_validator_app = Flask(__name__)


class StatusCache:
    """
    A cache of statuses to return for specific keys.

    The cache uses receipt data as a key and has a queue of statuses
    that are returned for that key.
    """

    def __init__(self):
        """
        Create a new cache.
        """
        self.store = defaultdict(list)

    @property
    def is_empty(self):
        """
        Returns:
            A boolean indicating if the cache is empty. An empty cache
            means that all enqueued status responses have been used.
        """
        return all((self.store[key] == [] for key in self.store))

    def next_status(self, key, **qualifiers):
        """
        Iterate through a key's queue to find the next status response
        that matches the provided qualifiers.
        Args:
            key:
                The key to fetch the next status for.
            **qualifiers:
                Additional qualifiers that the status must meet in order
                to be returned.

        Returns:
            The next matching status for the provided key if it exists
            or ``None`` if there is no matching status.
        """
        for response in self.store[key]:
            if response.get("qualifiers", {}) == qualifiers:
                self.store[key].remove(response)

                return response["status"]

        return None

    def queue_status(self, key, status, **qualifiers):
        """
        Add a new status to the queue for a specific key.

        Args:
            key:
                The key to enqueue the status for.
            status:
                The status response that will be returned.
            **qualifiers:
                Additional qualifiers that must be met in order for the
                response to be returned.
        """
        self.store[key].append({"qualifiers": qualifiers, "status": status})


status_cache = StatusCache()


@apple_validator_app.route("/", methods=["POST"])
def index():
    """
    Endpoint to mock the behavior of the Apple receipt validation
    service.
    """
    data = request.get_json()
    receipt_data = data.pop("receipt-data", None)

    response = status_cache.next_status(receipt_data, **data)
    if response is not None:
        return jsonify(response)

    return jsonify({"status": 21005})


@apple_validator_app.route("/_add-status", methods=["POST"])
def add_status():
    request_data = request.get_json()
    receipt_data = request_data.pop("receipt-data")
    status = request_data.pop("status")

    status_cache.queue_status(receipt_data, status, **request_data)

    return jsonify({"ok": True})


@apple_validator_app.route("/_status", methods=["GET"])
def server_status():
    return jsonify(
        {"is_empty": status_cache.is_empty, "store": status_cache.store}
    )


class AppleReceiptValidationClient(requests.Session):
    """
    Client for interacting with our mock receipt validation service.

    The client handles the additional test-related functionality such as
    enqueuing statuses.
    """

    ENQUEUE_ENDPOINT = "/_add-status"
    STATUS_ENDPONT = "/_status"

    def __init__(self, base_url, shared_secret):
        """
        Initialize a new client.

        Args:
            base_url:
                The base URL of the service to interact with.
            shared_secret:
                The shared secret to use for communication.
        """
        super().__init__()

        self.base_url = base_url
        self.shared_secret = shared_secret

    def enqueue_status(self, receipt_data, status_response):
        """
        Add a new status to the queue for a specific receipt.

        Args:
            receipt_data:
                The receipt data that the status should be queued for.
            status_response:
                The status response to add to the queue.
        """
        response = self.post(
            urljoin(
                self.base_url, AppleReceiptValidationClient.ENQUEUE_ENDPOINT
            ),
            json={
                "password": self.shared_secret,
                "receipt-data": receipt_data,
                "status": status_response,
            },
        )
        response.raise_for_status()

    def get_server_status(self):
        """
        Get the status of the mock server.

        Returns:
            A dictionary containing information about the current status
            of the mock server.
        """
        response = self.get(
            urljoin(self.base_url, AppleReceiptValidationClient.STATUS_ENDPONT)
        )
        response.raise_for_status()

        return response.json()
