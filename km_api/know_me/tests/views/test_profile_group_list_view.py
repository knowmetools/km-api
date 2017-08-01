from rest_framework import status

from know_me import serializers, views


profile_list_view = views.ProfileListView.as_view()


def test_create(api_rf, km_user_factory):
    """
    Sending a POST request with valid data to the view should create a
    new profile.
    """
    km_user = km_user_factory()

    api_rf.user = km_user.user

    data = {
        'name': 'New Group',
        'is_default': True,
    }

    request = api_rf.post(km_user.get_profile_list_url(), data)
    response = profile_list_view(request, pk=km_user.pk)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = serializers.ProfileListSerializer(
        km_user.profiles.get(),
        context={'request': request})

    assert response.data == serializer.data


def test_get_own(api_rf, profile_factory):
    """
    Users should be able to list their own km_user's profiles.
    """
    profile = profile_factory()
    km_user = profile.km_user
    user = km_user.user

    api_rf.user = user

    request = api_rf.get(km_user.get_profile_list_url())
    response = profile_list_view(request, pk=km_user.pk)

    serializer = serializers.ProfileListSerializer(
        km_user.profiles,
        context={'request': request},
        many=True)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data
