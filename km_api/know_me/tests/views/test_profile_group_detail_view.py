from rest_framework import status

from know_me import serializers, views


profile_group_detail_view = views.ProfileGroupDetailView.as_view()


def test_get_own_group(api_rf, profile_group_factory):
    """
    Users should be able to access groups that are a part of their own
    km_user.
    """
    group = profile_group_factory()
    km_user = group.km_user

    api_rf.user = km_user.user

    request = api_rf.get(group.get_absolute_url())
    response = profile_group_detail_view(request, pk=group.pk)

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
    km_user = group.km_user

    api_rf.user = km_user.user

    data = {
        'name': 'New Name',
    }

    request = api_rf.patch(group.get_absolute_url(), data)
    response = profile_group_detail_view(request, pk=group.pk)

    assert response.status_code == status.HTTP_200_OK

    group.refresh_from_db()
    serializer = serializers.ProfileGroupDetailSerializer(
        group,
        context={'request': request})

    assert response.data == serializer.data
