from unittest import mock

from rest_framework import status
from rest_framework.reverse import reverse

from account import serializers, views


password_reset_view = views.PasswordResetView.as_view()
url = reverse('account:reset-password')


def test_reset_password(api_rf, email_factory):
    """
    Sending a POST request with a verified email address should send a
    password reset to the provided email.
    """
    email = email_factory(verified=True)

    data = {
        'email': email.email,
    }

    request = api_rf.post(url, data)

    with mock.patch(
            'account.serializers.PasswordResetSerializer.save',
            autospec=True) as mock_save:
        response = password_reset_view(request)

    assert response.status_code == status.HTTP_200_OK
    assert mock_save.call_count == 1


def test_reset_password_invalid_email(api_rf):
    """
    If a malformed email address is submitted, the serializer's errors
    should be returned.
    """
    data = {
        'email': 'notrealemail',
    }

    request = api_rf.post(url, data)
    response = password_reset_view(request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    serializer = serializers.PasswordResetSerializer(data=data)
    assert not serializer.is_valid()

    assert response.data == serializer.errors
