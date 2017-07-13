from account import models


def test_create_email(user_factory):
    """
    Test creating an email.
    """
    email = models.EmailAddress.objects.create(
        email='test@example.com',
        user=user_factory())

    assert not email.verified


def test_string_conversion(email_factory):
    """
    Converting an email address to a string should return the actual
    email address associated with the instance.
    """
    email = email_factory()

    assert str(email) == email.email
