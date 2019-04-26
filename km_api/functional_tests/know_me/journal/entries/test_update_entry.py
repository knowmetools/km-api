from rest_framework import status


def test_update_anonymous(api_client, journal_entry_factory):
    """
    Anonymous users should receive a 403 response if they attempt to
    update a journal entry.
    """
    entry = journal_entry_factory()
    url = f"/know-me/journal/entries/{entry.pk}/"
    response = api_client.patch(url, {"text": "New text."})

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_as_owner(
    api_client, enable_premium_requirement, journal_entry_factory, user_factory
):
    """
    The owner of a journal entry should be able to update it.
    """
    # Assume Terry is an existing premium user.
    password = "password"
    user = user_factory(
        first_name="Terry", has_premium=True, password=password
    )
    api_client.log_in(user.primary_email.email, password)

    # If he has a journal entry...
    entry = journal_entry_factory(km_user__user=user, text="Old text.")

    # ...then he should be able to update it.
    data = {"text": "New text."}
    url = f"/know-me/journal/entries/{entry.pk}/"
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["text"] == data["text"]


def test_update_no_premium(
    api_client, enable_premium_requirement, journal_entry_factory, user_factory
):
    """
    If the owner of the journal entry does not have an active premium
    subscription, a 404 response should be returned when trying to
    update the entry.
    """
    # Assume Gina is a non-premium user with an existing journal
    # entry.
    password = "password"
    user = user_factory(first_name="Gina", password=password)
    entry = journal_entry_factory(km_user__user=user)

    # If she attempts to delete this entry, she should receive a 404
    # response.
    api_client.log_in(user.primary_email.email, password)
    url = f"/know-me/journal/entries/{entry.pk}/"
    response = api_client.patch(url, {"text": "New text."})

    assert response.status_code == status.HTTP_404_NOT_FOUND
