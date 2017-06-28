from rest_framework import status

from know_me import serializers, views


profile_detail_view = views.ProfileDetailView.as_view()


def test_get_anonymous(api_rf, profile_factory):
    """
    Anonymous users should not be able to access the view.
    """
    profile = profile_factory()

    request = api_rf.get(profile.get_absolute_url())
    response = profile_detail_view(request, profile_pk=profile.pk)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_other_profile(api_rf, profile_factory, user_factory):
    """
    A user should not be able to access profiles owned by a different
    user.
    """
    user = user_factory()
    api_rf.user = user

    # Create profile for different user
    profile = profile_factory()

    request = api_rf.get(profile.get_absolute_url())
    response = profile_detail_view(request, profile_pk=profile.pk)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_own_profile(api_rf, profile_factory, user_factory):
    """
    A user should be able to get the details of their own profile.
    """
    user = user_factory()
    api_rf.user = user

    profile = profile_factory(user=user)

    request = api_rf.get(profile.get_absolute_url())
    response = profile_detail_view(request, profile_pk=profile.pk)

    serializer = serializers.ProfileDetailSerializer(
        profile,
        context={'request': request})

    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data


def test_update(api_rf, profile_factory, user_factory):
    """
    Sending a PATCH request to the view should update the specified
    profile.
    """
    user = user_factory()
    api_rf.user = user

    profile = profile_factory(name='Jim', user=user)
    data = {
        'name': 'John',
    }

    request = api_rf.patch(profile.get_absolute_url(), data)
    response = profile_detail_view(request, profile_pk=profile.pk)

    assert response.status_code == status.HTTP_200_OK

    profile.refresh_from_db()
    serializer = serializers.ProfileDetailSerializer(
        profile,
        context={'request': request})

    assert response.data == serializer.data
