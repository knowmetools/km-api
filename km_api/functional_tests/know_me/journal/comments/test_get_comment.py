from rest_framework import status

from functional_tests import serialization_helpers
from test_utils import serialized_time


def test_get_comment_anonymous(api_client, entry_comment_factory):
    """
    Anonymous users should receive a 403 response if they try to fetch a
    comment on a journal entry.
    """
    comment = entry_comment_factory(entry__km_user__user__has_premium=True)

    url = f"/know-me/journal/comments/{comment.pk}/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_comment_as_author(
    api_client, entry_comment_factory, user_factory
):
    """
    The author of a comment should be able to retrieve it.
    """
    # Assume Shawn is an existing user.
    password = "password"
    user = user_factory(first_name="Shawn", password=password)
    api_client.log_in(user.primary_email.email, password)

    # If he makes a comment on a journal entry whose owner has an active
    # premium subscription...
    comment = entry_comment_factory(
        entry__km_user__user__has_premium=True, user=user
    )

    # ...he should be able to retrieve it.
    url = f"/know-me/journal/comments/{comment.pk}/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": comment.pk,
        "url": api_client.build_full_url(url),
        "created_at": serialized_time(comment.created_at),
        "updated_at": serialized_time(comment.updated_at),
        "permissions": {"destroy": True, "read": True, "write": True},
        "text": comment.text,
        "user": serialization_helpers.user_info(user),
    }


def test_get_comment_as_journal_owner(
    api_client, entry_comment_factory, user_factory
):
    """
    The author of a comment should be able to retrieve it.
    """
    # Assume Juliet is an existing user with an active premium
    # subscription.
    password = "password"
    user = user_factory(
        first_name="Juliet", has_premium=True, password=password
    )
    api_client.log_in(user.primary_email.email, password)

    # If there is a comment made on her journal entry...
    comment = entry_comment_factory(entry__km_user__user=user)

    # ...she should be able to retrieve it.
    url = f"/know-me/journal/comments/{comment.pk}/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": comment.pk,
        "url": api_client.build_full_url(url),
        "created_at": serialized_time(comment.created_at),
        "updated_at": serialized_time(comment.updated_at),
        "permissions": {"destroy": True, "read": True, "write": False},
        "text": comment.text,
        "user": serialization_helpers.user_info(comment.user),
    }


def test_get_comment_expired_subscription(
    api_client, enable_premium_requirement, entry_comment_factory, user_factory
):
    """
    If the owner of the journal entry that the comment was made on does
    not have an active premium subscription, the comment should be
    inaccessible.
    """
    # Assume Carleton is an existing user.
    password = "password"
    user = user_factory(first_name="Carleton", password=password)
    api_client.log_in(user.primary_email.email, password)

    # If he has made a comment on a journal entry whose owner has an
    # inactive premium subscription...
    comment = entry_comment_factory(user=user)

    # Then he should receive a 404 response when he tries to access that
    # comment.
    url = f"/know-me/journal/comments/{comment.pk}/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
