from rest_framework import status

from know_me import serializers, views


profile_item_detail_view = views.ProfileItemDetailView.as_view()


def test_anonymous(api_rf, profile_item_factory):
    """
    Anonymous users should not be able to access the view.
    """
    item = profile_item_factory()
    row = item.row
    group = row.group
    profile = group.profile

    request = api_rf.get(item.get_absolute_url())
    response = profile_item_detail_view(
        request,
        group_pk=group.pk,
        item_pk=item.pk,
        profile_pk=profile.pk,
        row_pk=row.pk)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_item(api_rf, profile_item_factory):
    """
    Users should be able to access items in their own profile.
    """
    item = profile_item_factory()
    row = item.row
    group = row.group
    profile = group.profile

    api_rf.user = profile.user

    request = api_rf.get(item.get_absolute_url())
    response = profile_item_detail_view(
        request,
        group_pk=group.pk,
        item_pk=item.pk,
        profile_pk=profile.pk,
        row_pk=row.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ProfileItemSerializer(
        item,
        context={'request': request})

    assert response.data == serializer.data


def test_update(api_rf, profile_item_factory):
    """
    Sending a PATCH request to the view with valid data should update
    the profile item with the given primary key.
    """
    item = profile_item_factory(name='Old Name')
    row = item.row
    group = row.group
    profile = group.profile

    api_rf.user = profile.user

    data = {
        'name': 'New Name',
    }

    request = api_rf.patch(item.get_absolute_url(), data)
    response = profile_item_detail_view(
        request,
        group_pk=group.pk,
        item_pk=item.pk,
        profile_pk=profile.pk,
        row_pk=row.pk)

    assert response.status_code == status.HTTP_200_OK

    item.refresh_from_db()
    serializer = serializers.ProfileItemSerializer(
        item,
        context={'request': request})

    assert response.data == serializer.data
