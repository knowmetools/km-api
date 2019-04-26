from rest_framework import status


def test_delete_anonymous(api_client, journal_entry_factory):
    """
    Anonymous users should receive a 403 response if they attempt to
    delete a journal entry.
    """
    entry = journal_entry_factory()
    url = f"/know-me/journal/entries/{entry.pk}/"
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_as_owner(
    api_client, enable_premium_requirement, journal_entry_factory, user_factory
):
    """
    The owner of a journal entry should be able to delete it.
    """
    # Assume Raymond is an existing premium user.
    password = "password"
    user = user_factory(
        first_name="Raymond", has_premium=True, password=password
    )
    api_client.log_in(user.primary_email.email, password)

    # If he has a journal entry...
    entry = journal_entry_factory(km_user__user=user)

    # ...then he should be able to delete it.
    url = f"/know-me/journal/entries/{entry.pk}/"
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_no_premium(
    api_client, enable_premium_requirement, journal_entry_factory, user_factory
):
    """
    If the owner of the journal entry does not have an active premium
    subscription, a 404 response should be returned when trying to
    delete the entry.
    """
    # Assume Charles is a non-premium user with an existing journal
    # entry.
    password = "password"
    user = user_factory(first_name="Charles", password=password)
    entry = journal_entry_factory(km_user__user=user)

    # If he attempts to delete this entry, he should receive a 404
    # response.
    api_client.log_in(user.primary_email.email, password)
    url = f"/know-me/journal/entries/{entry.pk}/"
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
