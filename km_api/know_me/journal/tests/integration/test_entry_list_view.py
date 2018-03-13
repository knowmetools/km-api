import pytest

from rest_framework import status
from rest_framework.reverse import reverse

from know_me.journal import serializers


@pytest.mark.integration
def test_create_entry(api_client, api_rf, km_user_factory):
    """
    Sending a POSt request to the view should create a new Journal Entry
    for the specified Know Me user.
    """
    km_user = km_user_factory()

    api_client.force_authenticate(user=km_user.user)
    api_rf.user = km_user.user

    data = {
        'text': 'My entry text.',
    }

    url = reverse('know-me:journal:entry-detail', kwargs={'pk': km_user.pk})
    request = api_rf.post(url, data)
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = serializers.EntryDetailSerializer(
        km_user.journal_entries.get(),
        context={'request': request})

    assert response.data == serializer.data


@pytest.mark.integration
def test_get_entry_list(api_client, api_rf, entry_factory, km_user_factory):
    """
    Sending a GET request to the view should return the specified Know
    Me user's journal entries.
    """
    km_user = km_user_factory()

    api_client.force_authenticate(user=km_user.user)
    api_rf.user = km_user.user

    url = reverse('know-me:journal:entry-detail', kwargs={'pk': km_user.pk})
    request = api_rf.get(url)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.EntryListSerializer(
        km_user.journal_entries.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data
