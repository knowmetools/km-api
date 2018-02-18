import hashlib

from mailing_list import models


def test_create(user_factory):
    """
    Test creating a new mailchimp user.
    """
    user = user_factory()
    subscriber_hash = hashlib.md5(
        user.primary_email.email.lower().encode('utf8')).hexdigest()

    models.MailchimpUser.objects.create(
        subscriber_hash=subscriber_hash,
        user=user)


def test_string_conversion(mailchimp_user_factory):
    """
    Converting a MailChimp user to a string should return the user's
    full name.
    """
    mailchimp_user = mailchimp_user_factory()
    user = mailchimp_user.user

    assert str(mailchimp_user) == user.get_full_name()
