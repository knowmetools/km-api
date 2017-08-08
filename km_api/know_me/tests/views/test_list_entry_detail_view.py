from rest_framework import status

from know_me import models, serializers, views

list_entry_detail_view = views.ListEntryDetailView.as_view()


def test_delete(api_rf, list_entry_factory):
    """
    Sending a DELETE request to the view should delete the item with
    the given ID.
    """
    entry = list_entry_factory()
    content = entry.list_content
    item = content.profile_item
    topic = item.topic
    profile = topic.profile
    km_user = profile.km_user

    api_rf.user = km_user.user

    request = api_rf.delete(entry)
    response = list_entry_detail_view(request, pk=entry.pk)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert models.ListEntry.objects.count() == 0


def test_get(api_rf, list_entry_factory):
    """
    Should return the list entry details.
    """
    entry = list_entry_factory()
    api_rf.user = entry.list_content.profile_item.topic.profile.km_user.user

    request = api_rf.get('/')
    response = list_entry_detail_view(request, pk=entry.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ListEntrySerializer(
            entry,
            context={'request': request})

    assert response.data == serializer.data


def test_update(api_rf, list_entry_factory):
    """
    Sending a PATCH request to the view with valid data should update
    the list entry with the given primary key.
    """
    entry = list_entry_factory(text='Old Text')
    content = entry.list_content
    item = content.profile_item
    topic = item.topic
    profile = topic.profile
    km_user = profile.km_user

    api_rf.user = km_user.user

    data = {
        'text': 'New Text',
    }

    request = api_rf.patch('/', data)
    response = list_entry_detail_view(request, pk=entry.pk)

    assert response.status_code == status.HTTP_200_OK

    entry.refresh_from_db()
    serializer = serializers.ListEntrySerializer(
            entry,
            context={'request': request})

    assert response.data == serializer.data
