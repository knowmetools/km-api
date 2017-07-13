from account import models


def test_create_initial(user_factory):
    """
    The first email address associated with a user should be made the
    primary address.
    """
    email = models.EmailAddress.objects.create(
        email='test@example.com',
        user=user_factory())

    assert email.primary


def test_create_secondary_email(email_factory, user_factory):
    """
    If the user already has an email address, the next one should not be
    automatically set as the primary.
    """
    user = user_factory()
    email_factory(user=user)

    email = models.EmailAddress.objects.create(
        email='test2@example.com',
        user=user)

    assert not email.primary
