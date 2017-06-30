from rest_framework import status

from know_me import serializers, views


profile_group_detail_view = views.ProfileGroupDetailView.as_view()


def test_get_anonymous(api_rf, profile_group_factory):
    """
    Anonymous users should not be able to access the view.
    """
    group = profile_group_factory()
    profile = group.profile

    request = api_rf.get(group.get_absolute_url())
    response = profile_group_detail_view(
        request,
        group_pk=group.pk,
        profile_pk=profile.pk)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_own_group(api_rf, profile_group_factory):
    """
    Users should be able to access groups that are a part of their own
    profile.
    """
    group = profile_group_factory()
    profile = group.profile

    api_rf.user = profile.user

    request = api_rf.get(group.get_absolute_url())
    response = profile_group_detail_view(
        request,
        group_pk=group.pk,
        profile_pk=profile.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ProfileGroupDetailSerializer(
        group,
        context={'request': request})

    assert response.data == serializer.data


def test_update(api_rf, profile_group_factory):
    """
    Sending a PATCH request to the view with valid data should update
    the specified profile group.
    """
    group = profile_group_factory(name='Old Name')
    profile = group.profile

    api_rf.user = profile.user

    data = {
        'name': 'New Name',
    }

    request = api_rf.patch(group.get_absolute_url(), data)
    response = profile_group_detail_view(
        request,
        group_pk=group.pk,
        profile_pk=profile.pk)

    assert response.status_code == status.HTTP_200_OK

    group.refresh_from_db()
    serializer = serializers.ProfileGroupDetailSerializer(
        group,
        context={'request': request})

    assert response.data == serializer.data
