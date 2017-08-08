from rest_framework import status

from know_me import serializers, views

list_entry_list_view = views.ListEntryListView.as_view()


def test_create(api_rf, list_content_factory):
    """
    Sending a POST request to the view with valid data should create a
    new list entry.
    """
    list_content = list_content_factory()
    item = list_content.profile_item
    topic = item.topic
    profile = topic.profile
    km_user = profile.km_user

    api_rf.user = km_user.user

    data = {
        'text': 'New Text',
    }

    request = api_rf.post(
            list_content.get_list_entry_list_url(),
            data,
            format='json')
    response = list_entry_list_view(request, pk=list_content.pk)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = serializers.ListEntrySerializer(
            list_content.entries.get(),
            context={'request': request})

    assert response.data == serializer.data


def test_get_entries(api_rf, list_entry_factory, list_content_factory):
    """
    This view should return a list of list entries belonging to the
    list content.
    """
    content = list_content_factory()
    list_entry_factory(list_content=content)
    list_entry_factory(list_content=content)

    item = content.profile_item
    topic = item.topic
    profile = topic.profile
    km_user = profile.km_user

    api_rf.user = km_user.user

    request = api_rf.get(content.get_list_entry_list_url())
    response = list_entry_list_view(request, pk=content.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ListEntrySerializer(
            content.entries.all(),
            context={'request': request},
            many=True)

    assert response.data == serializer.data
