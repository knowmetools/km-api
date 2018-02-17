from rest_framework import status

from know_me import serializers, views

category_list_view = views.MediaResourceCategoryListView.as_view()


def test_create(api_rf, km_user_factory):
    """
    Sending a POST request with valid data to the view should create a
    new media resource category.
    """
    km_user = km_user_factory()

    api_rf.user = km_user.user

    data = {
        'name': 'Category',
    }

    request = api_rf.post(km_user.get_media_resource_category_list_url(), data)
    response = category_list_view(request, pk=km_user.pk)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = serializers.MediaResourceCategorySerializer(
        km_user.media_resource_categories.get(),
        context={'request': request})

    assert response.data == serializer.data


def test_get_own(api_rf, media_resource_category_factory):
    """
    Users should be able to list their own km_user's media resource category.
    """
    media_resource_category = media_resource_category_factory()
    km_user = media_resource_category.km_user
    user = km_user.user

    api_rf.user = user

    request = api_rf.get(km_user.get_media_resource_category_list_url())
    response = category_list_view(request, pk=km_user.pk)

    serializer = serializers.MediaResourceCategorySerializer(
            km_user.media_resource_categories,
            context={'request': request},
            many=True)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data
