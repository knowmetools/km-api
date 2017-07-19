import pytest

from rest_framework import status
from rest_framework.reverse import reverse

from account import serializers, views


email_verification_view = views.EmailVerificationView.as_view()
url = reverse('account:verify-email')


def test_verify_email(
        api_rf,
        email_confirmation_factory,
        email_factory,
        user_factory):
    """
    Sending a POST request with a valid key to the view should verify
    the email confirmation with that key.
    """
    user = user_factory(password='password')
    email = email_factory(user=user)
    confirmation = email_confirmation_factory(email=email)

    data = {
        'key': confirmation.key,
        'password': 'password',
    }

    request = api_rf.post(url, data)
    response = email_verification_view(request)

    assert response.status_code == status.HTTP_200_OK

    email.refresh_from_db()

    assert email.verified


@pytest.mark.django_db
def test_verify_email_invalid_key(api_rf):
    """
    Sending an invalid request to the view should display the errors
    from the view's serializer.
    """
    data = {
        'key': 'invalidkey',
    }

    request = api_rf.post(url, data)
    response = email_verification_view(request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    serializer = serializers.EmailVerificationSerializer(data=data)
    assert not serializer.is_valid()

    assert response.data == serializer.errors
