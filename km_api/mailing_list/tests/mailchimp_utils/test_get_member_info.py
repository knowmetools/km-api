from mailing_list import mailchimp_utils


def test_get_info(user_factory):
    """
    This method should generate data to use for a MailChimp list member
    from a user instance.
    """
    user = user_factory()
    expected = {
        'email_address': user.email,
        'merge_fields': {
            'FNAME': user.first_name,
            'LNAME': user.last_name,
        },
    }

    assert mailchimp_utils.get_member_info(user) == expected
