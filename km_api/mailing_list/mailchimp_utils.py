"""Utilities for interacting with MailChimp.
"""

import logging

from django.conf import settings

import mailchimp3

from requests.exceptions import HTTPError

from mailing_list import models


logger = logging.getLogger(__name__)


def get_member_info(user):
    """
    Generate info for a MailChimp list member.

    This method maps data from the given user into a format that
    MailChimp understands.

    Args:
        user:
            The user to generate info for.

    Returns:
        dict:
            A dictionary containing the user's information in a format
            readable by MailChimp.
    """
    return {
        'email_address': user.primary_email.email,
        'merge_fields': {
            'FNAME': user.first_name,
            'LNAME': user.last_name,
        },
    }


def sync_mailchimp_data(list_id, user):
    """
    Sync user data to MailChimp.

    If there is no existing link to MailChimp for the user, ie no
    ``MailchimpUser`` instance for the user, we subscribe a new member
    to the mailing list. For a member already on the list, their details
    are updated to match those of the given user.

    Args:
        list_id (str):
            The ID of the MailChimp list to add the user to.
        user:
            The user to pull information for the mailing list from.
    """
    mailchimp_query = models.MailchimpUser.objects.filter(user=user)

    if mailchimp_query.exists():
        mailchimp_user = mailchimp_query.get()

        _member_update(list_id, user, mailchimp_user)
    else:
        _member_create(list_id, user)


def _get_client():
    """
    Get a MailChimp client.

    Returns:
        An instance of ``mailchimp3.MailChimp`` with the credentials
        specified in the project's settings.
    """
    return mailchimp3.MailChimp('km-api', settings.MAILCHIMP_API_KEY)


def _member_create(list_id, user):
    """
    Create a member for a MailChimp list.

    If the member already exists in the given list, we save a record of
    the membership and attempt to update their info.

    Args:
        list_id (str):
            The ID of the list to add a member to.
        user:
            The user to pull member info from.
    """
    client = _get_client()

    data = get_member_info(user)
    data.update({'status': 'subscribed'})

    try:
        response = client.lists.members.create(
            data=data,
            list_id=list_id)
        logger.info('Subscribed %s to mailing list', user.primary_email.email)
    except HTTPError:
        # When updating a user's info we don't want to set them to
        # subscribed
        del data['status']

        response = client.lists.members.update(
            data=data,
            list_id=list_id,
            subscriber_hash=user.primary_email.email)

        logger.info(
            ('Failed to create new mailing list member; updated info for %s '
             'instead.'),
            user.primary_email.email)

    models.MailchimpUser.objects.create(
        subscriber_hash=response['id'],
        user=user)


def _member_update(list_id, user, mailchimp_user):
    """
    Update a mailing list member's information.

    If the member does not exist, we add the member and update our
    record of their membership.

    Args:
        list_id (str):
            The ID of the list to update the member's info for.
        user:
            The user to pull member info from.
        mailchimp_user:
            The model instance linking the mailing list member to a user
            account. The instance will be updated to reflect the updated
            user information.
    """
    client = _get_client()

    data = get_member_info(user)

    try:
        response = client.lists.members.update(
            data=data,
            list_id=list_id,
            subscriber_hash=mailchimp_user.subscriber_hash)
        logger.info(
            'Updated mailing list info for %s.',
            user.primary_email.email)
    except HTTPError:
        data.update({'status': 'subscribed'})

        response = client.lists.members.create(
            data=data,
            list_id=list_id)

        logger.info(
            ('Failed to update member info; subscribed %s to mailing list '
             'instead.'),
            user.primary_email.email)

    mailchimp_user.subscriber_hash = response['id']
    mailchimp_user.save()
