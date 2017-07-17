from unittest import mock

from account import models


def test_create_no_key(settings, user_factory):
    """
    If no key is given, one should be randomly generated.
    """
    settings.PASSWORD_RESET_KEY_LENGTH = 3

    with mock.patch(
            'account.managers.get_random_string',
            autospec=True,
            return_value='random') as mock_random:
        reset = models.PasswordReset.objects.create(user=user_factory())

    assert mock_random.call_count == 1
    assert mock_random.call_args[1] == {
        'length': settings.PASSWORD_RESET_KEY_LENGTH,
    }

    assert reset.key == mock_random.return_value


def test_create_with_key(user_factory):
    """
    If a key is provided, it should override the default.
    """
    reset = models.PasswordReset.objects.create(
        key='key',
        user=user_factory())

    assert reset.key == 'key'
