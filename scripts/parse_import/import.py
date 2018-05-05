#!/usr/bin/env python

import argparse
import logging
import os

from parse_rest.connection import register
from parse_rest.user import User

from tqdm import tqdm

from api_client import APIClient


logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
rootLogger = logging.getLogger()

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)
rootLogger.setLevel(logging.INFO)


logger = logging.getLogger(__name__)


# Response returned from the API if that user has already been added
DUPLICATE_USER_MSG = 'legacy user with this email already exists.'


class ImproperlyConfiguredException(Exception):
    """
    Exception indicating the script was improperly configured.
    """


def delete_users(client):
    """
    Delete all legacy users previously uploaded to the API.

    Args:
        client:
            The client used to interact with the API.
    """
    users = list(client.legacy_user_list())

    for user in tqdm(users):
        client.legacy_user_delete(user)


def get_parser():
    """
    Get parser for command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Tool for exporting existing users from old Parse backend '
                    'to new API.',
    )

    parser.add_argument(
        '-d',
        '--delete',
        action='store_true',
        help='Delete all previously uploaded users',
    )

    # Manage connection to Parse
    parser.add_argument(
        '--parse-api-root',
        action='store',
        default=os.environ.get('PARSE_API_ROOT', ''),
        help='API root of the Parse application to connect to. Defaults to '
             'the value of the PARSE_API_ROOT environment variable.',
    )
    parser.add_argument(
        '--parse-app-id',
        action='store',
        default=os.environ.get('PARSE_APP_ID', ''),
        help='ID of the Parse application to connect to. Defaults to the '
             'value of the PARSE_APP_ID environment variable.',
    )
    parser.add_argument(
        '--parse-master-key',
        action='store',
        default=os.environ.get('PARSE_MASTER_KEY', ''),
        help='Master key of the Parse application to connect to. Defaults to '
             'the value of the PARSE_MASTER_KEY environment variable.',
    )

    # Manage connection to new API
    parser.add_argument(
        '--api-root',
        action='store',
        default=os.environ.get('API_ROOT', ''),
        help='Root of the new API to upload users to. Defaults to the value '
             'of the API_ROOT environment variable.',
    )
    parser.add_argument(
        '--admin-email',
        action='store',
        default=os.environ.get('ADMIN_EMAIL', ''),
        help='Email address of the admin user used to connect to the new API.',
    )
    parser.add_argument(
        '--admin-password',
        action='store',
        default=os.environ.get('ADMIN_PASSWORD', ''),
        help='Password of the admin user used to connect to the new API.',
    )

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    client = APIClient(args.api_root)
    client.login(args.admin_email, args.admin_password)

    # We don't need Parse credentials for a delete operation, so we
    # perform it early and bail.
    if args.delete:
        delete_users(client)
        return None

    parse_connect(
        args.parse_api_root,
        args.parse_app_id,
        args.parse_master_key,
    )

    upload_users(client)


def parse_connect(api_root, app_id, master_key):
    """
    Register a connection to the Parse application.

    Args:
        api_root:
            The root of the Parse API.
        app_id:
            The ID of the Parse application to connect to.
        master_key:
            The master key to use when connecting to Parse. This key
            grants the admin permissions required by the script.
    """
    if not api_root:
        raise ImproperlyConfiguredException(
            'The root of the Parse API was not specified.',
        )

    if not app_id or not master_key:
        raise ImproperlyConfiguredException(
            'Make sure both the app ID and master key for the Parse '
            'application have been specified.',
        )

    os.environ['PARSE_API_ROOT'] = api_root

    # The empty string is the REST_API_KEY, which is not necessary when
    # the master key is used.
    register(app_id, '', master_key=master_key)


def upload_users(client):
    url = '{}/know-me/legacy-users/'.format(client.api_root)

    user_count = User.Query.all().count()
    logger.info('Uploading %d users', user_count)

    for user in tqdm(User.Query.all().limit(user_count)):
        if not hasattr(user, 'email'):
            logger.warning('User %s does not have an email', user)
            continue

        response = client.session.post(
            url,
            data={
                'email': user.email,
            },
        )

        if response.status_code == 400:
            body = response.json()
            email_error = body.get('email')

            if email_error is not None:
                if DUPLICATE_USER_MSG in email_error:
                    logger.debug(
                        'Skipping user %s because they have already been '
                        'added.',
                        user.email,
                    )
                    continue

            logger.warning(
                'Failed to add user %s. Received response: %s',
                user.email,
                body,
            )
            continue

        response.raise_for_status()

        logger.debug('Uploaded user %s', user.email)


if __name__ == '__main__':
    main()
