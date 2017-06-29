from rest_framework import status

from know_me import serializers, views


profile_group_list_view = views.ProfileGroupListView.as_view()


def test_create(api_rf, profile_factory):
    """
    Sending a POST request with valid data to the view should create a
    new profile group.
    """
    profile = profile_factory()

    api_rf.user = profile.user

    data = {
        'name': 'New Group',
        'is_default': True,
    }

    request = api_rf.post(profile.get_group_list_url(), data)
    response = profile_group_list_view(request, profile_pk=profile.pk)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = serializers.ProfileGroupListSerializer(
        profile.groups.get(),
        context={'request': request})

    assert response.data == serializer.data


def test_get_anonymous(api_rf, profile_factory):
    """
    Anonymous users should not be able to access the view.
    """
    profile = profile_factory()

    request = api_rf.get(profile.get_group_list_url())
    response = profile_group_list_view(request, profile_pk=profile.pk)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_other(api_rf, profile_group_factory, user_factory):
    """
    User's should not be able to access the groups for a profile they
    don't own.
    """
    group = profile_group_factory()
    profile = group.profile

    api_rf.user = user_factory()

    request = api_rf.get(profile.get_group_list_url())
    response = profile_group_list_view(request, profile_pk=profile.pk)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_own(api_rf, profile_group_factory):
    """
    User's should be able to list their own profile's groups.
    """
    group = profile_group_factory()
    profile = group.profile
    user = profile.user

    api_rf.user = user

    request = api_rf.get(profile.get_group_list_url())
    response = profile_group_list_view(request, profile_pk=profile.pk)

    serializer = serializers.ProfileGroupListSerializer(
        profile.groups,
        context={'request': request},
        many=True)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data
