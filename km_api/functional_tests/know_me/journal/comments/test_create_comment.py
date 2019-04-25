from rest_framework import status


def test_create_comment_as_anonymous(api_client, journal_entry_factory):
    """
    Attempting to create a comment as an anonymous user should return a
    403 response code.
    """
    entry = journal_entry_factory(km_user__user__has_premium=True)
    url = f"/know-me/journal/entries/{entry.pk}/comments/"
    response = api_client.post(url, {"text": "Anonymous comment."})

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_new_comment(
    api_client,
    enable_premium_requirement,
    km_user_accessor_factory,
    journal_entry_factory,
    user_factory,
):
    """
    If the owner of a journal entry has a premium subscription, all
    users with access to the journal should be able to comment on the
    entry.
    """
    # Assume Sarah is an existing user.
    password = "password"
    user = user_factory(first_name="Sarah", password=password)
    api_client.log_in(user.primary_email.email, password)

    # If she has access to a premium user's journal...
    accessor = km_user_accessor_factory(
        is_accepted=True,
        km_user__user__has_premium=True,
        user_with_access=user,
    )
    entry = journal_entry_factory(km_user=accessor.km_user)

    # ...then she should be able to comment on the premium user's
    # journal entries.
    data = {"text": "Sample comment text."}
    url = f"/know-me/journal/entries/{entry.pk}/comments/"
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["text"] == data["text"]


def test_create_new_comment_no_premium(
    api_client,
    enable_premium_requirement,
    km_user_accessor_factory,
    journal_entry_factory,
    user_factory,
):
    """
    If the owner of a journal entry does not have an active premium
    subscription users should receive a 404 response if they attempt to
    comment on a journal entry.
    """
    # Assume Bill is an existing user.
    password = "password"
    user = user_factory(first_name="Bill", password=password)
    api_client.log_in(user.primary_email.email, password)

    # If he has access to a non-premium user's journal...
    accessor = km_user_accessor_factory(
        is_accepted=True,
        km_user__user__has_premium=False,
        user_with_access=user,
    )
    entry = journal_entry_factory(km_user=accessor.km_user)

    # ...then he should receive a 404 response if he attempts to comment
    # on a journal entry.
    data = {"text": "Sample comment text."}
    url = f"/know-me/journal/entries/{entry.pk}/comments/"
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
