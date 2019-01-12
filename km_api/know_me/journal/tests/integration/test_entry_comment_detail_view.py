import pytest

from rest_framework import status

from know_me.journal import models, serializers


@pytest.mark.integration
def test_delete_comment(api_client, entry_comment_factory):
    """
    Sending a DELETE request to the view should delete the specified
    comment.
    """
    comment = entry_comment_factory()
    api_client.force_authenticate(user=comment.user)

    url = comment.get_absolute_url()
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not models.EntryComment.objects.exists()


@pytest.mark.integration
def test_delete_comment_as_journal_owner(
    api_client, entry_factory, entry_comment_factory, km_user_factory
):
    """
    The journal owner should be able to delete journal comments left by
    other users.

    Regression test for #371
    """
    km_user = km_user_factory()
    api_client.force_authenticate(user=km_user.user)

    entry = entry_factory(km_user=km_user)
    comment = entry_comment_factory(entry=entry)

    url = comment.get_absolute_url()
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not models.EntryComment.objects.exists()


@pytest.mark.integration
def test_get_comment(api_client, api_rf, entry_comment_factory):
    """
    Sending a GET request to the view should return the information of
    the specified comment.
    """
    comment = entry_comment_factory()
    api_client.force_authenticate(user=comment.user)
    api_rf.user = comment.user

    url = comment.get_absolute_url()
    request = api_rf.get(url)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.EntryCommentSerializer(
        comment, context={"request": request}
    )

    assert response.data == serializer.data


@pytest.mark.integration
def test_patch_update_comment(api_client, entry_comment_factory):
    """
    Sending a PATCH request to the view should update the specified
    comment with the provided information.
    """
    comment = entry_comment_factory(text="Old comment text.")
    api_client.force_authenticate(user=comment.user)

    data = {"text": "New comment text."}

    url = comment.get_absolute_url()
    response = api_client.patch(url, data)

    comment.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert comment.text == data["text"]
