from rest_framework import status

from know_me import serializers, views


profile_item_list_view = views.ProfileItemListView.as_view()


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
        'image_content': {},
    }

    request = api_rf.post(topic.get_item_list_url(), data, format='json')
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


def test_get_shared_items(
        api_rf,
        km_user_accessor_factory,
        km_user_factory,
        profile_item_factory,
        profile_topic_factory,
        user_factory):
    """
    Users who were granted access to a profile through an accessor
    should be able to list its profile items.
    """
    user = user_factory()
    topic = profile_topic_factory()
    km_user = topic.profile.km_user
    km_user_accessor_factory(
        accepted=True,
        km_user=km_user,
        user_with_access=user)

    profile_item_factory(topic=topic)
    profile_item_factory(topic=topic)

    api_rf.user = user

    request = api_rf.get(topic.get_item_list_url())
    response = profile_item_list_view(request, pk=topic.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ProfileItemSerializer(
        topic.items.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data


def test_get_shared_items_not_accepted(
        api_rf,
        km_user_accessor_factory,
        km_user_factory,
        profile_item_factory,
        profile_topic_factory,
        user_factory):
    """
    Users who were granted access to a profile through an accessor that
    hasn't been accepted should not be able to list profile items.
    """
    user = user_factory()
    topic = profile_topic_factory()
    km_user = topic.profile.km_user
    km_user_accessor_factory(
        accepted=False,
        km_user=km_user,
        user_with_access=user)

    profile_item_factory(topic=topic)
    profile_item_factory(topic=topic)

    api_rf.user = user

    request = api_rf.get(topic.get_item_list_url())
    response = profile_item_list_view(request, pk=topic.pk)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_shared_items_private_profile(
        api_rf,
        km_user_accessor_factory,
        profile_factory,
        profile_item_factory,
        profile_topic_factory,
        user_factory):
    """
    The view should return items in private profiles if the user has
    private profile access.
    """
    profile = profile_factory(is_private=True)
    topic = profile_topic_factory(profile=profile)

    km_user = profile.km_user
    user = user_factory()

    km_user_accessor_factory(
        accepted=True,
        has_private_profile_access=True,
        km_user=km_user,
        user_with_access=user)

    profile_item_factory(topic=topic)
    profile_item_factory(topic=topic)

    api_rf.user = user

    request = api_rf.get(topic.get_item_list_url())
    response = profile_item_list_view(request, pk=topic.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ProfileItemSerializer(
        topic.items.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data


def test_get_shared_items_private_profile_no_access(
        api_rf,
        km_user_accessor_factory,
        profile_factory,
        profile_topic_factory,
        user_factory):
    """
    The view should not return entries in private profiles if the user
    doesn't have private profile access.
    """
    profile = profile_factory(is_private=True)
    topic = profile_topic_factory(profile=profile)

    km_user = profile.km_user
    user = user_factory()

    km_user_accessor_factory(
        accepted=True,
        has_private_profile_access=False,
        km_user=km_user,
        user_with_access=user)

    api_rf.user = user

    request = api_rf.get(topic.get_item_list_url())
    response = profile_item_list_view(request, pk=topic.pk)

    assert response.status_code == status.HTTP_404_NOT_FOUND
