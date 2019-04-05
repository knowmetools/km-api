from rest_framework import status


def test_delete_comment_anonymous(
    api_client, entry_comment_factory, subscription_factory
):
    """
    Anonymous users should receive a 403 response if they try to
    delete a comment on a journal entry.
    """
    comment = entry_comment_factory()
    subscription_factory(is_active=True, user=comment.entry.km_user.user)

    url = f"/know-me/journal/comments/{comment.pk}/"
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_comment_as_journal_owner(
    api_client, entry_comment_factory, subscription_factory, user_factory
):
    """
    The owner of the journal that a comment was made on should be able
    to delete the comment.

    Regression test for #371.
    """
    # If Sally is a journal owner with an active premium subscription...
    password = "password"
    user = user_factory(first_name="Sally", password="password")
    subscription_factory(is_active=True, user=user)
    api_client.log_in(user.primary_email.email, password)

    # ...and a comment is made on an entry in her journal
    comment = entry_comment_factory(entry__km_user__user=user)

    # ...then she should be able to delete it.
    url = f"/know-me/journal/comments/{comment.pk}/"
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_comment_as_owner(
    api_client, entry_comment_factory, subscription_factory, user_factory
):
    """
    The owner of a comment should be able to delete it.
    """
    # Given Jason, an existing user...
    password = "password"
    user = user_factory(first_name="Jason", password=password)
    api_client.log_in(user.primary_email.email, password)

    # If he makes a comment on an entry whose owner has an active
    # premium subscription...
    comment = entry_comment_factory(user=user)
    subscription_factory(is_active=True, user=comment.entry.km_user.user)

    # ...he should be able to delete it.
    url = f"/know-me/journal/comments/{comment.pk}/"
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
