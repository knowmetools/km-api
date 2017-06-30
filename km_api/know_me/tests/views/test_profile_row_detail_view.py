from rest_framework import status

from know_me import serializers, views


profile_row_detail_view = views.ProfileRowDetailView.as_view()


def test_anonymous(api_rf, profile_row_factory):
    """
    Anonymous users should not be able to access the view.
    """
    row = profile_row_factory()
    group = row.group
    profile = group.profile

    request = api_rf.get(row.get_absolute_url())
    response = profile_row_detail_view(
        request,
        group_pk=group.pk,
        profile_pk=profile.pk,
        row_pk=row.pk)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_own_row(api_rf, profile_row_factory):
    """
    Users should be able to access rows that are part of their own
    profile.
    """
    row = profile_row_factory()
    group = row.group
    profile = group.profile

    api_rf.user = profile.user

    request = api_rf.get(row.get_absolute_url())
    response = profile_row_detail_view(
        request,
        group_pk=group.pk,
        profile_pk=profile.pk,
        row_pk=row.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ProfileRowSerializer(
        row,
        context={'request': request})

    assert response.data == serializer.data


def test_update(api_rf, profile_row_factory):
    """
    Sending a PATCH request to the view with valid data should update
    the given row.
    """
    row = profile_row_factory(name='Old Name')
    group = row.group
    profile = group.profile

    api_rf.user = profile.user

    data = {
        'name': 'New Name',
    }

    request = api_rf.patch(row.get_absolute_url(), data)
    response = profile_row_detail_view(
        request,
        group_pk=group.pk,
        profile_pk=profile.pk,
        row_pk=row.pk)

    assert response.status_code == status.HTTP_200_OK

    row.refresh_from_db()
    serializer = serializers.ProfileRowSerializer(
        row,
        context={'request': request})

    assert response.data == serializer.data
