"""Factories for generating test instances of ``mailing_list`` models.
"""

import hashlib

import factory

from mailing_list import models


class MailchimpUserFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``MailchimpUser`` instances.
    """
    user = factory.SubFactory('factories.UserFactory')

    class Meta:
        model = models.MailchimpUser

    @factory.lazy_attribute
    def subscriber_hash(self):
        """
        Generate a hash of a user's email address.

        Returns:
            str:
                The MD5 hash of the user's lowercased email.
        """
        email = self.user.primary_email.email.lower()

        return hashlib.md5(email.encode('utf8')).hexdigest()
