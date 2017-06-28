from rest_framework import status
from rest_framework.reverse import reverse

from know_me import serializers, views


profile_list_view = views.ProfileListView.as_view()
url = reverse('know-me:profile-list')


def test_create(api_rf, user_factory):
    """
    Sending a POST request with valid data to the view should create a
    new profile for the user making the request.
    """
    user = user_factory()
    api_rf.user = user

    data = {
        'name': user.get_short_name(),
        'quote': "Hi, I'm {name}".format(name=user.get_short_name()),
        'welcome_message': 'Welcome to my profile',
    }

    request = api_rf.post(url, data)
    response = profile_list_view(request)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = serializers.ProfileListSerializer(user.profile)

    assert response.data == serializer.data


def test_create_second_profile(api_rf, profile_factory, user_factory):
    """
    A user who already has a profile should not be able to create a
    second one.
    """
    user = user_factory()
    api_rf.user = user

    profile_factory(user=user)

    data = {
        'name': user.get_short_name(),
        'quote': "Hi, I'm {name}".format(name=user.get_short_name()),
        'welcome_message': 'Welcome to my profile',
    }

    request = api_rf.post(url, data)
    response = profile_list_view(request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_anonymous(api_rf, profile_factory):
    """
    Anonymous users should not be able to access the view.
    """
    request = api_rf.get(url)
    response = profile_list_view(request)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_other_profile(api_rf, profile_factory, user_factory):
    """
    The profile list should not include other users' profiles.
    """
    user = user_factory()
    api_rf.user = user

    # Build profile for different user
    profile_factory()

    request = api_rf.get(url)
    response = profile_list_view(request)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


def test_get_own_profile(api_rf, profile_factory, user_factory):
    """
    If the requesting user has a profile, then a GET request to this
    view should contain that profile.
    """
    user = user_factory()
    api_rf.user = user

    profile = profile_factory(user=user)

    request = api_rf.get(url)
    response = profile_list_view(request)

    serializer = serializers.ProfileListSerializer([profile], many=True)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data
