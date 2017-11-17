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


def test_get_shared_entries(
        api_rf,
        km_user_accessor_factory,
        km_user_factory,
        list_entry_factory,
        list_content_factory,
        user_factory):
    """
    Users who were granted access to a profile through an accessor
    should be able to view list entries.
    """
    user = user_factory()
    content = list_content_factory()
    km_user = content.profile_item.topic.profile.km_user
    km_user_accessor_factory(
        accepted=True,
        km_user=km_user,
        user_with_access=user)

    list_entry_factory(list_content=content)
    list_entry_factory(list_content=content)

    api_rf.user = user

    request = api_rf.get(content.get_list_entry_list_url())
    response = list_entry_list_view(request, pk=content.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ListEntrySerializer(
        content.entries.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data


def test_get_shared_entries_not_accepted(
        api_rf,
        km_user_accessor_factory,
        km_user_factory,
        list_entry_factory,
        list_content_factory,
        user_factory):
    """
    The view should not return entries whose access was granted through
    an accessor that has not been accepted.
    """
    user = user_factory()
    content = list_content_factory()
    km_user = content.profile_item.topic.profile.km_user
    km_user_accessor_factory(
        accepted=False,
        km_user=km_user,
        user_with_access=user)

    list_entry_factory(list_content=content)
    list_entry_factory(list_content=content)

    api_rf.user = user

    request = api_rf.get(content.get_list_entry_list_url())
    response = list_entry_list_view(request, pk=content.pk)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_shared_entries_private_profile(
        api_rf,
        km_user_accessor_factory,
        list_entry_factory,
        list_content_factory,
        profile_factory,
        profile_item_factory,
        profile_topic_factory,
        user_factory):
    """
    The view should return entries in private profiles if the user has
    private profile access.
    """
    profile = profile_factory(is_private=True)
    topic = profile_topic_factory(profile=profile)
    item = profile_item_factory(topic=topic)
    content = list_content_factory(profile_item=item)

    km_user = profile.km_user
    user = user_factory()

    km_user_accessor_factory(
        accepted=True,
        has_private_profile_access=True,
        km_user=km_user,
        user_with_access=user)

    list_entry_factory(list_content=content)
    list_entry_factory(list_content=content)

    api_rf.user = user

    request = api_rf.get(content.get_list_entry_list_url())
    response = list_entry_list_view(request, pk=content.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ListEntrySerializer(
        content.entries.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data


def test_get_shared_entries_private_profile_no_access(
        api_rf,
        km_user_accessor_factory,
        list_content_factory,
        profile_factory,
        profile_item_factory,
        profile_topic_factory,
        user_factory):
    """
    The view should not return entries whose access was granted through
    an accessor that has not been accepted.
    """
    profile = profile_factory(is_private=True)
    topic = profile_topic_factory(profile=profile)
    item = profile_item_factory(topic=topic)
    content = list_content_factory(profile_item=item)

    km_user = profile.km_user
    user = user_factory()

    km_user_accessor_factory(
        accepted=True,
        has_private_profile_access=False,
        km_user=km_user,
        user_with_access=user)

    api_rf.user = user

    request = api_rf.get(content.get_list_entry_list_url())
    response = list_entry_list_view(request, pk=content.pk)

    assert response.status_code == status.HTTP_404_NOT_FOUND
