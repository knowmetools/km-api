from unittest import mock

from django.conf import settings

from account import models


def test_create_default_key(user_factory):
    """
    If no key is given, one should be randomly generated using Django's
    secure ``get_random_string`` function.
    """
    with mock.patch(
            'account.managers.get_random_string',
            autospec=True,
            return_value='randomstring') as mock_random:
        confirmation = models.EmailConfirmation.objects.create(
            user=user_factory())

    assert mock_random.call_count == 1
    assert mock_random.call_args[1] == {
        'length': settings.EMAIL_CONFIRMATION_KEY_LENGTH,
    }

    assert confirmation.key == mock_random.return_value


def test_create_with_key(user_factory):
    """
    If a key is provided, it should be used instead of the default.
    """
    confirmation = models.EmailConfirmation.objects.create(
        key='key',
        user=user_factory())

    assert confirmation.key == 'key'
