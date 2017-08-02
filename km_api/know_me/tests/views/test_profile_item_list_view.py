from rest_framework import status

from know_me import serializers, views


profile_item_list_view = views.ProfileItemListView.as_view()


def test_anonymous(api_rf, profile_topic_factory):
    """
    Anonymous users should not be able to access the view.
    """
    topic = profile_topic_factory()

    request = api_rf.get(topic.get_item_list_url())
    response = profile_item_list_view(request, pk=topic.pk)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create(api_rf, profile_topic_factory):
    """
    Sending a POST request to the view with valid data should create a
    new profile item.
    """
    topic = profile_topic_factory()
    profile = topic.profile
    km_user = profile.km_user

    api_rf.user = km_user.user

    data = {
        'name': 'Test Item',
    }

    request = api_rf.post(topic.get_item_list_url(), data)
    response = profile_item_list_view(request, pk=topic.pk)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = serializers.ProfileItemSerializer(
        topic.items.get(),
        context={
            'km_user': km_user,
            'request': request,
        })

    assert response.data == serializer.data


def test_get_items(api_rf, profile_item_factory, profile_topic_factory):
    """
    This view should return a serialized list of profile items belonging
    to the given topic.
    """
    topic = profile_topic_factory()
    profile_item_factory(topic=topic)
    profile_item_factory(topic=topic)

    profile = topic.profile
    km_user = profile.km_user

    api_rf.user = km_user.user

    request = api_rf.get(topic.get_item_list_url())
    response = profile_item_list_view(request, pk=topic.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ProfileItemSerializer(
        topic.items.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data
