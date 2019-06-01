from rest_framework import status


def test_create_profile(api_client, enable_premium_requirement, user_factory):
    """
    Premium users should be able to create profiles.
    """
    password = "password"
    user = user_factory(
        has_premium=True, password=password, registration_signal__send=True
    )
    api_client.log_in(user.primary_email.email, password)

    url = f"/know-me/users/{user.km_user.pk}/profiles/"
    data = {"name": "Test Profile"}
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == data["name"]
