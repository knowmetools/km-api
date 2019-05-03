from rest_email_auth.models import EmailConfirmation
from rest_framework import status


URL = "/account/register/"


def test_register_primary_email(api_client):
    """
    Registering for an account should set the email used to register as
    the user's primary email address.

    Regression test for #468
    """
    email = "test@example.com"
    password = "sup3rc0mplexpassw0rd"
    data = {
        "email": email,
        "first_name": "John",
        "last_name": "Smith",
        "password": password,
    }

    # If John registers for an account...
    response = api_client.post(URL, data)

    assert response.status_code == status.HTTP_201_CREATED

    # ...and we simulate him verifying his email...
    EmailConfirmation.objects.get().confirm()

    # ...then the email he signed up with should be set to his primary
    # email.
    api_client.log_in(email, password)
    response = api_client.get("/account/emails/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["email"] == email
    assert response.json()[0]["is_primary"]
