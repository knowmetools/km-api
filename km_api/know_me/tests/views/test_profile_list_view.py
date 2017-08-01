from rest_framework import status
from rest_framework.reverse import reverse

from know_me import serializers, views


km_user_list_view = views.KMUserListView.as_view()
url = reverse('know-me:km-user-list')


def test_create(api_rf, user_factory):
    """
    Sending a POST request with valid data to the view should create a
    new km_user for the user making the request.
    """
    user = user_factory()
    api_rf.user = user

    data = {
        'name': user.get_short_name(),
        'quote': "Hi, I'm {name}".format(name=user.get_short_name()),
    }

    request = api_rf.post(url, data)
    response = km_user_list_view(request)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = serializers.KMUserListSerializer(
        user.km_user,
        context={'request': request})

    assert response.data == serializer.data


def test_create_second_km_user(api_rf, km_user_factory, user_factory):
    """
    A user who already has a km_user should not be able to create a
    second one.
    """
    user = user_factory()
    api_rf.user = user

    km_user_factory(user=user)

    data = {
        'name': user.get_short_name(),
        'quote': "Hi, I'm {name}".format(name=user.get_short_name()),
    }

    request = api_rf.post(url, data)
    response = km_user_list_view(request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_own_km_user(api_rf, km_user_factory, user_factory):
    """
    If the requesting user has a km_user, then a GET request to this
    view should contain that km_user.
    """
    user = user_factory()
    api_rf.user = user

    km_user = km_user_factory(user=user)

    request = api_rf.get(url)
    response = km_user_list_view(request)

    serializer = serializers.KMUserListSerializer(
        [km_user],
        context={'request': request},
        many=True)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data
