from unittest import mock

from rest_framework import status
from rest_framework.reverse import reverse

from account import serializers, views


password_change_view = views.PasswordChangeView.as_view()
url = reverse('account:change-password')


def test_anonymous(api_rf):
    """
    Anonymous users should not be able to access the view.
    """
    request = api_rf.post(url, {})
    response = password_change_view(request)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_change_password(api_rf, user_factory):
    """
    Sending a valid POST request to the view should change the
    requesting user's password.
    """
    user = user_factory(password='oldpassword')
    api_rf.user = user

    data = {
        'new_password': 'newpassword',
        'old_password': 'oldpassword',
    }

    request = api_rf.post(url, data)

    with mock.patch('account.views.update_session_auth_hash') as mock_hash:
        response = password_change_view(request)

    assert response.status_code == 200
    assert user.check_password(data['new_password'])

    # Ensure the session hash was updated
    assert mock_hash.call_count == 1
    assert mock_hash.call_args[0][1] == user


def test_invalid_request(api_rf, user_factory):
    """
    If an invalid request is submitted, the response should contain an
    error message.
    """
    user = user_factory()
    api_rf.user = user

    request = api_rf.post(url, {})
    response = password_change_view(request)

    serializer = serializers.PasswordChangeSerializer(
        context={'request': request},
        data={})
    assert not serializer.is_valid()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == serializer.errors
