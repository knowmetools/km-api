from rest_framework import status

from functional_tests.know_me.journal import serialization_helpers


def test_get_anonymous(api_client, journal_entry_factory):
    """
    Anonymous users should receive a 403 response if they attempt to
    get a journal entry.
    """
    entry = journal_entry_factory()
    url = f"/know-me/journal/entries/{entry.pk}/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_as_owner(
    api_client, enable_premium_requirement, journal_entry_factory, user_factory
):
    """
    The owner of a journal entry should be able to retrieve it.
    """
    # Assume Rosa is an existing premium user.
    password = "password"
    user = user_factory(first_name="Rosa", has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    # If she has a journal entry...
    entry = journal_entry_factory(km_user__user=user)

    # ...then she should be able to retrieve it.
    url = f"/know-me/journal/entries/{entry.pk}/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == serialization_helpers.serialize_entry(
        entry, api_client.build_full_url
    )


def test_get_no_premium(
    api_client, enable_premium_requirement, journal_entry_factory, user_factory
):
    """
    If the owner of the journal entry does not have an active premium
    subscription, a 404 response should be returned when trying to
    retrieve the entry.
    """
    # Assume Amy is a non-premium user with an existing journal
    # entry.
    password = "password"
    user = user_factory(first_name="Amy", password=password)
    entry = journal_entry_factory(km_user__user=user)

    # If she attempts to retrieve this entry, she should receive a 404
    # response.
    api_client.log_in(user.primary_email.email, password)
    url = f"/know-me/journal/entries/{entry.pk}/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
