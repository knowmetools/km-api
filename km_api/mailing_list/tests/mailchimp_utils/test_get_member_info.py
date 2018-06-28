from mailing_list import mailchimp_utils


def test_get_info(user_factory):
    """
    This method should generate data to use for a MailChimp list member
    from a user instance.
    """
    user = user_factory()
    expected = {
        'email_address': user.primary_email.email,
        'merge_fields': {
            'FNAME': user.first_name,
            'LNAME': user.last_name,
        },
    }

    assert mailchimp_utils.get_member_info(user) == expected


def test_get_member_info_no_primary_email(user_factory):
    """
    If the user does not have a primary email address, None should be
    returned.
    """
    user = user_factory()
    user.email_addresses.all().delete()

    assert mailchimp_utils.get_member_info(user) is None
