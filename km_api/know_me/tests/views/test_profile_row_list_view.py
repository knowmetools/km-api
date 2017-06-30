from rest_framework import status

from know_me import models, serializers, views


profile_row_list_view = views.ProfileRowListView.as_view()


def test_anonymous(api_rf, profile_group_factory):
    """
    Anonymous users should not be able to access the view.
    """
    group = profile_group_factory()
    profile = group.profile

    request = api_rf.get(group.get_row_list_url())
    response = profile_row_list_view(
        request,
        group_pk=group.pk,
        profile_pk=profile.pk)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_row(api_rf, profile_group_factory):
    """
    Sending a POST request with valid data to the view should create a
    new row.
    """
    group = profile_group_factory()
    profile = group.profile

    api_rf.user = profile.user

    data = {
        'name': 'Test Row',
        'row_type': models.ProfileRow.TEXT,
    }

    request = api_rf.post(group.get_row_list_url(), data)
    response = profile_row_list_view(
        request,
        group_pk=group.pk,
        profile_pk=profile.pk)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = serializers.ProfileRowSerializer(
        group.rows.get(),
        context={'request': request})

    assert response.data == serializer.data


def test_list_own_rows(api_rf, profile_row_factory):
    """
    Users should be able to list the rows in their own profile.
    """
    row = profile_row_factory()
    group = row.group
    profile = group.profile

    api_rf.user = profile.user

    request = api_rf.get(group.get_row_list_url())
    response = profile_row_list_view(
        request,
        group_pk=group.pk,
        profile_pk=profile.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ProfileRowSerializer(
        [row],
        context={'request': request},
        many=True)

    assert response.data == serializer.data
