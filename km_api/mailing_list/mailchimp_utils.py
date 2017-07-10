"""Utilities for interacting with MailChimp.
"""


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
