from rest_framework import status

from know_me import serializers, views


profile_detail_view = views.ProfileDetailView.as_view()


def test_get_own_profile(api_rf, profile_factory):
    """
    A user should be able to get the details of their own Know Me user
    account.
    """
    profile = profile_factory()
    km_user = profile.km_user

    api_rf.user = km_user.user

    request = api_rf.get(profile.get_absolute_url())
    response = profile_detail_view(request, pk=profile.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ProfileDetailSerializer(
        profile,
        context={'request': request})

    assert response.data == serializer.data


def test_update(api_rf, profile_factory):
    """
    Sending a PATCH request to the view should update the specified
    Know Me user.
    """
    profile = profile_factory(name='Old Name')
    km_user = profile.km_user

    api_rf.user = km_user.user

    data = {
        'name': 'New Name',
    }

    request = api_rf.patch(profile.get_absolute_url(), data)
    response = profile_detail_view(request, pk=profile.pk)

    assert response.status_code == status.HTTP_200_OK

    profile.refresh_from_db()
    serializer = serializers.ProfileDetailSerializer(
        profile,
        context={'request': request})

    assert response.data == serializer.data
