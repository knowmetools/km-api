from rest_framework import status


def test_update_comment_anonymous(api_client, entry_comment_factory):
    """
    Anonymous users should receive a 403 response if they try to update
    a comment.
    """
    comment = entry_comment_factory()

    url = f"/know-me/journal/comments/{comment.pk}/"
    response = api_client.patch(url, {"text": "New text."})

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_comment_as_author(
    api_client, entry_comment_factory, user_factory
):
    """
    The owner of a comment should be able to edit it.
    """
    # If Rachel is a user...
    password = "password"
    user = user_factory(first_name="Rachel", password=password)
    api_client.log_in(user.primary_email.email, password)

    # ...and she creates a comment...
    comment = entry_comment_factory(text="Old comment text.", user=user)

    # ...then she should be able to update the comment with new text.
    text = "New comment text."
    url = f"/know-me/journal/comments/{comment.pk}/"
    response = api_client.patch(url, {"text": text})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["text"] == text


def test_update_comment_as_journal_owner(
    api_client, entry_comment_factory, user_factory
):
    """
    The owner of the journal entry that a comment was made on should not
    be able to edit the comment.
    """
    # Assume Joey is an existing user.
    password = "password"
    user = user_factory(first_name="Joey", password=password)
    api_client.log_in(user.primary_email.email, password)

    # If there is a comment made on one of his journal entries...
    comment = entry_comment_factory(entry__km_user__user=user)

    # ...then he should not be able to edit it.
    url = f"/know-me/journal/comments/{comment.pk}/"
    response = api_client.patch(url, {"text": "New text."})

    assert response.status_code == status.HTTP_403_FORBIDDEN
