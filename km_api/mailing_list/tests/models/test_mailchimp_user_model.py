import hashlib

from mailing_list import models


def test_create(user_factory):
    """
    Test creating a new mailchimp user.
    """
    user = user_factory()
    subscriber_hash = hashlib.md5(
        user.email.lower().encode('utf8')).hexdigest()

    models.MailchimpUser.objects.create(
        subscriber_hash=subscriber_hash,
        user=user)
