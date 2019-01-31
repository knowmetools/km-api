from rest_framework import status


def test_verify_email(
    api_client, email_confirmation_factory, email_factory, user_factory
):
    """
    Sending a POST request to the email verification endpoint with a
    valid confirmation key should mark the email address as verified.
    """
    user = user_factory()
    email = email_factory(user=user)
    confirmation = email_confirmation_factory(email=email)

    response = api_client.post(
        "/account/verify-email/", json={"key": confirmation.key}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"email": email.email}
