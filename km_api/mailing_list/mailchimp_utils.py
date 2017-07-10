"""Utilities for interacting with MailChimp.
"""

from django.conf import settings

import mailchimp3

from mailing_list import models


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
        'email_address': user.email,
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
    client = _get_client()

    mailchimp_query = models.MailchimpUser.objects.filter(user=user)

    if mailchimp_query.exists():
        mailchimp_user = mailchimp_query.get()

        response = client.lists.members.update(
            data=get_member_info(user),
            list_id=list_id,
            subscriber_hash=mailchimp_user.subscriber_hash)

        mailchimp_user.subscriber_hash = response['id']
        mailchimp_user.save()
    else:
        member_data = get_member_info(user)
        member_data.update({'status': 'subscribed'})

        response = client.lists.members.create(
            data=member_data,
            list_id=list_id)

        models.MailchimpUser.objects.create(
            subscriber_hash=response['id'],
            user=user)


def _get_client():
    """
    Get a MailChimp client.

    Returns:
        An instance of ``mailchimp3.MailChimp`` with the credentials
        specified in the project's settings.
    """
    return mailchimp3.MailChimp('km-api', settings.MAILCHIMP_API_KEY)
