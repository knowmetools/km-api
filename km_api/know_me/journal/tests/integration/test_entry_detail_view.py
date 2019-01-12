import pytest

from rest_framework import status

from know_me.journal import models, serializers


@pytest.mark.integration
def test_delete_entry(api_client, entry_factory):
    """
    Sending a DELETE request to the view should delete the specified
    journal entry.
    """
    entry = entry_factory()
    api_client.force_authenticate(user=entry.km_user.user)

    url = entry.get_absolute_url()
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert models.Entry.objects.count() == 0


@pytest.mark.integration
def test_get_entry(api_client, api_rf, entry_factory):
    """
    Sending a GET request to the view should return the information of
    the specified journal entry.
    """
    entry = entry_factory()
    user = entry.km_user.user

    api_client.force_authenticate(user=user)
    api_rf.user = user

    url = entry.get_absolute_url()
    request = api_rf.get(url)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.EntryDetailSerializer(
        entry, context={"request": request}
    )

    assert response.data == serializer.data


@pytest.mark.integration
def test_patch_entry(api_client, entry_factory):
    """
    Sending a PATCH request to the view should update the specified
    journal entry with the provided information.
    """
    entry = entry_factory(text="Old Text")
    api_client.force_authenticate(user=entry.km_user.user)

    data = {"text": "New Text"}

    url = entry.get_absolute_url()
    response = api_client.patch(url, data)

    entry.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert entry.text == data["text"]
