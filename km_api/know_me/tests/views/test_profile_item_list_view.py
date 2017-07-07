from rest_framework import status

from know_me import serializers, views


profile_item_list_view = views.ProfileItemListView.as_view()


def test_anonymous(api_rf, profile_row_factory):
    """
    Anonymous users should not be able to access the view.
    """
    row = profile_row_factory()

    request = api_rf.get(row.get_item_list_url())
    response = profile_item_list_view(request, pk=row.pk)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create(api_rf, gallery_item_factory, profile_row_factory):
    """
    Sending a POST request to the view with valid data should create a
    new profile item.
    """
    row = profile_row_factory()
    group = row.group
    profile = group.profile
    gallery_item = gallery_item_factory(profile=profile)

    api_rf.user = profile.user

    data = {
        'gallery_item': gallery_item.pk,
        'name': 'Test Item',
        'text': 'Some sample text.',
    }

    request = api_rf.post(row.get_item_list_url(), data)
    response = profile_item_list_view(request, pk=row.pk)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = serializers.ProfileItemSerializer(
        row.items.get(),
        context={
            'profile': profile,
            'request': request,
        })

    assert response.data == serializer.data


def test_get_items(api_rf, profile_item_factory, profile_row_factory):
    """
    This view should return a serialized list of profile items belonging
    to the given row.
    """
    row = profile_row_factory()
    profile_item_factory(row=row)
    profile_item_factory(row=row)

    group = row.group
    profile = group.profile

    api_rf.user = profile.user

    request = api_rf.get(row.get_item_list_url())
    response = profile_item_list_view(request, pk=row.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ProfileItemSerializer(
        row.items.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data
