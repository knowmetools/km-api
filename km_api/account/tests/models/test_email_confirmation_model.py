from account import models


def test_create(user_factory):
    """
    Test creating a new email confirmation.
    """
    models.EmailConfirmation.objects.create(
        key='key',
        user=user_factory())


def test_string_conversion(email_confirmation_factory):
    """
    Converting an email confirmation to a string should return a message
    indicating who the confirmation is for.
    """
    confirmation = email_confirmation_factory()
    expected = 'Confirmation for {email}'.format(email=confirmation.user.email)

    assert str(confirmation) == expected
