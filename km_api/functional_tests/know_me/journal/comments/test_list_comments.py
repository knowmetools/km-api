from rest_framework import status

from functional_tests.know_me.journal import serialization_helpers


def test_list_comments_as_anonymous(api_client, journal_entry_factory):
    """
    Attempting to list comments as an anonymous user should return a 404
    response code.
    """
    entry = journal_entry_factory(km_user__user__has_premium=True)
    url = f"/know-me/journal/entries/{entry.pk}/comments/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_list_comments_as_owner(
    api_client,
    enable_premium_requirement,
    journal_entry_factory,
    journal_entry_comment_factory,
    user_factory,
):
    """
    The journal owner should be able to list the comments made on any of
    their journal entries.
    """
    # Assume Jake is a journal owner with a premium subscription.
    password = "password"
    user = user_factory(first_name="Jake", has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    # If Jake has a journal entry that has comments on it...
    entry = journal_entry_factory(km_user__user=user)
    c1 = journal_entry_comment_factory(entry=entry)
    c2 = journal_entry_comment_factory(entry=entry)

    # ...then he should be able to list those comments.
    url = f"/know-me/journal/entries/{entry.pk}/comments/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == serialization_helpers.serialize_comment(
        [c1, c2], api_client.build_full_url, is_list=True
    )


def test_list_comments_no_premium(
    api_client,
    enable_premium_requirement,
    journal_entry_factory,
    journal_entry_comment_factory,
    user_factory,
):
    """
    If the owner of the journal that en entry exists in does not have an
    active premium subscription, attempting to list comments on an entry
    should return a 404 response.
    """
    # Assume Amy is an existing user without an active premium
    # subscription.
    password = "password"
    user = user_factory(first_name="Amy", password=password)
    api_client.log_in(user.primary_email.email, password)

    # If she has a journal entry...
    entry = journal_entry_factory(km_user__user=user)

    # ...then trying to list the comments for it should return a 404
    # response.
    url = f"/know-me/journal/entries/{entry.pk}/comments/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
