from collections import namedtuple
import logging

import requests


logger = logging.getLogger(__name__)


LegacyUser = namedtuple(
    'LegacyUser',
    [
        'id',
        'url',
        'created_at',
        'updated_at',
        'email',
    ],
)


class APIClient(object):
    """
    Client for interacting with the new Know Me API.
    """
    LEGACY_USER_LIST_ENDPOINT = '/know-me/legacy-users/'
    LOGIN_ENDPOINT = '/auth/login/'

    def __init__(self, api_root):
        """
        Instantiate a new API client.

        Args:
            api_root:
                The root URL that the API is accessible from.
        """
        self.api_root = api_root
        self.session = requests.Session()

    def legacy_user_delete(self, user):
        """
        Delete a legacy user.

        Args:
            user:
                The user to delete.
        """
        response = self.session.delete(user.url)
        response.raise_for_status()

        logger.debug('Deleted user %s', user.email)

    def legacy_user_list(self):
        """
        List all legacy users.

        Yields:
            All the legacy users in the API.
        """
        url = '{}{}'.format(self.api_root, self.LEGACY_USER_LIST_ENDPOINT)

        while url is not None:
            response = self.session.get(url)
            response.raise_for_status()

            data = response.json()
            url = data['next']

            for user_data in data['results']:
                yield LegacyUser(**user_data)

    def login(self, email, password):
        """
        Authenticate the client.

        Args:
            email:
                The user's email.
            password:
                The user's password.
        """
        if not email:
            raise ValueError('An email address must be provided.')

        if not password:
            raise ValueError('A password must be provided.')

        url = '{root}{path}'.format(
            path=self.LOGIN_ENDPOINT,
            root=self.api_root,
        )
        response = self.session.post(
            url,
            data={
                'email': email,
                'password': password,
            },
        )
        response.raise_for_status()

        self.session.headers.update(
            {'Authorization': 'Token {}'.format(response.json()['token'])},
        )

        logger.debug('Succesfully logged in as %s', email)
