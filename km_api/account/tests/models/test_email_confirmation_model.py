from account import models


def test_create(user_factory):
    """
    Test creating a new email confirmation.
    """
    models.EmailConfirmation.objects.create(
        key='key',
        user=user_factory())
