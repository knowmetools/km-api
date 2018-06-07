import pytest

from rest_framework import status

from know_me.profile import serializers


@pytest.mark.integration
def test_create_list_entry(api_client, api_rf, profile_item_factory):
    """
    Sending a POST request to the view should create a new list entry
    for the specified profile item.
    """
    item = profile_item_factory()
    user = item.topic.profile.km_user.user

    api_client.force_authenticate(user=user)
    api_rf.user = user

    data = {
        'text': 'Test list entry text.',
    }

    url = item.get_list_entries_url()
    request = api_rf.post(url, data)
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED

    item.refresh_from_db()
    serializer = serializers.ListEntrySerializer(
        item.list_entries.get(),
        context={'request': request})

    assert response.data == serializer.data


@pytest.mark.integration
def test_get_list_entries(
        api_client,
        api_rf,
        list_entry_factory,
        profile_item_factory):
    """
    Sending a GET request to the view should list the list entries
    attached to the specified profile item.
    """
    item = profile_item_factory()
    list_entry_factory(profile_item=item)
    list_entry_factory(profile_item=item)
    list_entry_factory()

    user = item.topic.profile.km_user.user
    api_client.force_authenticate(user=user)
    api_rf.user = user

    url = item.get_list_entries_url()
    request = api_rf.get(url)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ListEntrySerializer(
        item.list_entries.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data


@pytest.mark.integration
def test_put_profile_order(
        api_client,
        api_rf,
        list_entry_factory,
        profile_item_factory):
    """
    Sending a PUT request to the view should set the order of the user's
    profiles.
    """
    item = profile_item_factory()
    user = item.topic.profile.km_user.user

    api_client.force_authenticate(user=user)
    api_rf.user = user

    l1 = list_entry_factory(profile_item=item)
    l2 = list_entry_factory(profile_item=item)
    l3 = list_entry_factory(profile_item=item)

    data = {
        'order': [l1.id, l3.id, l2.id],
    }

    url = item.get_list_entries_url()
    request = api_rf.put(url, data)
    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ListEntrySerializer(
        item.list_entries.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data
    assert list(item.get_listentry_order()) == data['order']
