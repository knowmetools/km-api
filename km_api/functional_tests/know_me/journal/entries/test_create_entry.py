from rest_framework import status


def test_create_entry_as_owner(
    api_client, enable_premium_requirement, user_factory
):
    """
    If the owner of a journal has an active premium subscription, they
    should be able to create new journal entries.
    """
    # Assume John is an existing premium user.
    password = "password"
    user = user_factory(
        first_name="John",
        has_premium=True,
        password=password,
        registration_signal__send=True,
    )
    api_client.log_in(user.primary_email.email, password)

    # He should be able to create a new journal entry.
    url = f"/know-me/users/{user.km_user.pk}/journal-entries/"
    data = {"text": "Test journal entry."}
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["text"] == data["text"]
