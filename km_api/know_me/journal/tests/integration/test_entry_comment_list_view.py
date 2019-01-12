import pytest

from rest_framework import status

from know_me.journal import serializers


@pytest.mark.integration
def test_get_comment_list(
    api_client, api_rf, entry_comment_factory, entry_factory
):
    """
    Sending a GET request to the view should return a list of the
    comments attached to the specified journal entry.
    """
    entry = entry_factory()
    user = entry.km_user.user

    entry_comment_factory(entry=entry)
    entry_comment_factory(entry=entry)
    entry_comment_factory()

    api_client.force_authenticate(user=user)
    api_rf.user = user

    url = entry.get_comments_url()
    request = api_rf.get(url)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.EntryCommentSerializer(
        entry.comments.all(), context={"request": request}, many=True
    )

    assert response.data == serializer.data


@pytest.mark.integration
def test_post_new_comment(api_client, api_rf, entry_factory):
    """
    Sending a POST request to the view should create a new comment on
    the specified journal entry.
    """
    entry = entry_factory()
    user = entry.km_user.user

    api_client.force_authenticate(user=user)
    api_rf.user = user

    data = {"text": "My comment text."}

    url = entry.get_comments_url()
    request = api_rf.post(url, data)
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = serializers.EntryCommentSerializer(
        entry.comments.get(), context={"request": request}
    )

    assert response.data == serializer.data
