import pytest

from rest_framework import status
from rest_framework.reverse import reverse


url = reverse('rest-email-auth:register')


@pytest.mark.integration
def test_register(api_client, db):
    """
    Sending a POST request to the registration endpoint should use our
    custom registration serializer to register the new user.

    This is a regression test for #244, mainly to ensure that the custom
    fields added to our registration serializer are accepted.
    """
    data = {
        'email': 'test@example.com',
        'password': 'uncommon-passw0rd',
        'first_name': 'John',
        'last_name': 'Doe',
    }

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
